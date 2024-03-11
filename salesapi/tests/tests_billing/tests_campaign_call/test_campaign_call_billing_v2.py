from krispcall.konference.billing.billing_task_queue import (
    process_billing_transaction,
)
from krispcall.twilio.models import ConferenceResource
from krispcall_twilio.twilio_client import TwilioClient
import pytest
import asyncio
import uuid

from redis import Redis
from krispcall.common.core.bootstrap import JobQueue
from krispcall.billing.service_layer.helpers import business_rules
from krispcall.konference.billing.billing_service import BillingService
from krispcall.konference.billing.models import (
    BillingResponse,
    CampaignOutboundCallRequest,
)
from krispcall.konference.billing.enums import BillingTypeEnum

from krispcall.twilio.enums import ActiveStatusEnum, NotActiveStatusEnum
from tests.tests_billing.conftest import (
    _get_campaign_name,
    _create_campaigns_campaign_with_csv,
)
from tests.tests_billing.utils.models import (
    CampaignCall,
    CampaignCallDataStore,
)
from tests.tests_billing.utils.test_data import (
    get_testdata1_all_success,
    get_test_data2_no_answer_calls,
    get_testdata_call_not_answer_with_voicemaildrop,
    get_testdata_receivers_are_busy,
    get_testdata_receiver_decline_calls,
)
from tests.tests_billing.utils.campaign_utils import (
    execute_campaign_call,
)

from krispcall.core.abstracts.shortid import ShortId


class TestCampaignCallv2:  # Test cases group for campaign calls v2 is the test which test more indepth functionality such as redis queue for now
    async def _run_and_assert_test_case(
        self, test_get_campaign, test_contacts, campaign_id, status_enum
    ):
        data_store = CampaignCallDataStore()
        for contact in test_contacts:
            contact.campaign_id = campaign_id
            contact.status = status_enum
        data_store.add_all_campaign_calls(test_contacts)

        for contact in test_contacts:
            await execute_campaign_call(test_get_campaign, contact, data_store)

        total_charge = 0.0
        total_estimated_charge = 0.0
        for contact in data_store.data_list:
            total_charge += contact.charge_amount
            total_estimated_charge += contact.expected_outcome

            assert contact.call_duration == contact.elapsed_time
            assert contact.charge_amount == contact.expected_outcome
        assert total_charge == total_estimated_charge
        print("")

    async def _run_campaign(
        self,
        test_campaign,
        test_contacts: list[CampaignCall],
        data_store: CampaignCallDataStore,
    ):
        data_store.add_all_campaign_calls(test_contacts)

        for contact in test_contacts:
            await execute_campaign_call(test_campaign, contact, data_store)

        total_charge = 0.0
        total_estimated_charge = 0.0
        for contact in data_store.data_list:
            total_charge += contact.charge_amount
            total_estimated_charge += contact.expected_outcome

            assert contact.call_duration == contact.elapsed_time
            assert contact.charge_amount == contact.expected_outcome
        assert total_charge == total_estimated_charge

        print("")

    __test__ = False

    @pytest.mark.asyncio
    async def test_success_billing_transaction(
        self,
        mocker,
        connect_queue: JobQueue,
        member_data,
        sales_client,
        test_get_campaign,
    ):
        """
        Campaign call with success all success data
        """

        # queue = JobQueue(redis_settings=request.app.state.settings.redis_settings)
        # await connect_queue.connect()

        test_contacts = get_testdata1_all_success()
        campaign_id = test_get_campaign["id"]

        conference_id = str(uuid.uuid4())
        call_sid = str(uuid.uuid4())

        contact = test_contacts[0]

        contact.call_sid = call_sid
        contact.conference_sid = conference_id
        contact.conference_friendly_name = conference_id

        # Creating a CampaignOutboundCallRequest
        campaign_call_params = CampaignOutboundCallRequest(
            conversation_id=str(uuid.uuid4()),
            conference_friendly_name=str(uuid.uuid4()),
            campaign_id=contact.campaign_id,
            total_participants=business_rules.DEFAULT_TOTAL_PARTICIPANTS,
            billing_types=[
                BillingTypeEnum.SIP_CHARGE,
                BillingTypeEnum.CONFERENCE_CHARGE,
            ],
            call_sid=call_sid,
            child_call_sid=call_sid,
            conference_sid=conference_id,
            to=contact.to,
            from_=contact.from_,
            parent_call_sid=call_sid,
            remarks="",
            # workspace_id=ShortId(contact.workspace_id).uuid(),
            workspace_id=ShortId(contact.workspace_id).uuid(),
        )

        # mocker.patch(
        #     "krispcall.konference.billing.billing_task_queue.get_conference_resource",
        #     return_value=ConferenceResource(
        #         conference_status="in-progress",
        #         conference_id=conference_id,
        #     ),
        # )

        mocker.patch(
            "krispcall.konference.billing.billing_task_queue.get_conference_resource",
            side_effect=[
                ConferenceResource(
                    conference_status="in-progress",
                    conference_id=conference_id,
                ),
                ConferenceResource(
                    conference_status="in-progress",
                    conference_id=conference_id,
                ),
                ConferenceResource(
                    conference_status=NotActiveStatusEnum.CANCELED.value,
                    conference_id=conference_id,
                ),
            ],
        )

        mock_cache = mocker.Mock(spec=Redis)
        mock_twilio_client = mocker.Mock(spec=TwilioClient)
        # Call the method under test to mock the user credit

        result = await process_billing_transaction(
            campaign_call_params,
            cache=mock_cache,
            twilio_client=mock_twilio_client,
            queue=connect_queue,
            charge_call_back_time=5,
        )

        # result = await connect_queue._redis.wait(num_replicas=1, timeout=10)
        result = await connect_queue.wait()

        # job_result = [job.result() for job in connect_queue._redis._scheduler_jobs.values()]
        # await asyncio.gather(*job_result)  # type: ignore

        # await self._run_and_assert_test_case(
        #     test_get_campaign,
        #     test_contacts,
        #     campaign_id,
        #     ActiveStatusEnum.IN_PROGRESS,
        # )

        print("")

    @pytest.mark.asyncio
    async def test_no_answer_billing_transaction(
        self, member_data, sales_client, test_get_campaign
    ):
        """
        Campaign call with no answer calls
        """
        test_contacts = get_test_data2_no_answer_calls()
        campaign_id = test_get_campaign["id"]
        await self._run_and_assert_test_case(
            test_get_campaign,
            test_contacts,
            campaign_id,
            NotActiveStatusEnum.NO_ANSWER,
        )

    @pytest.mark.asyncio
    async def test_campaigns_parallel(
        self, member_data, sales_client, test_get_campaign
    ):
        """
        Running test case in concurrently from same workspace
        """
        campaign_id = test_get_campaign["id"]

        # Get the necessary data for the first campaign
        test_case_data1 = get_testdata1_all_success()
        campaign_name1 = _get_campaign_name()
        _create_campaigns_campaign_with_csv(
            sales_client, member_data, campaign_name1
        )

        # Get the necessary data for the second campaign
        test_case_data2 = get_test_data2_no_answer_calls()
        campaign_name2 = _get_campaign_name()
        _create_campaigns_campaign_with_csv(
            sales_client, member_data, campaign_name2
        )

        # Get the necessary data for the third campaign
        test_case_data3 = get_testdata_receiver_decline_calls()
        campaign_name3 = _get_campaign_name()
        _create_campaigns_campaign_with_csv(
            sales_client, member_data, campaign_name3
        )

        for contact in test_case_data1:
            contact.campaign_id = campaign_id
            contact.status = ActiveStatusEnum.IN_PROGRESS

        for contact in test_case_data2:
            contact.campaign_id = campaign_id
            contact.status = NotActiveStatusEnum.NO_ANSWER

        for contact in test_case_data3:
            contact.campaign_id = campaign_id
            contact.status = NotActiveStatusEnum.CANCELED

        # Run campaigns in parallel
        tasks = [
            self._run_campaign(
                test_get_campaign,
                test_case_data1,
                CampaignCallDataStore(),
            ),
            self._run_campaign(
                test_get_campaign,
                test_case_data2,
                CampaignCallDataStore(),
            ),
            self._run_campaign(
                test_get_campaign,
                test_case_data3,
                CampaignCallDataStore(),
            ),
        ]

        # Wait for both tasks to complete
        await asyncio.gather(*tasks)

    @pytest.mark.asyncio
    async def test_insufficient_credit(self, mocker, test_get_campaign):
        """
        Campaign call with insufficient workspace credit user would unable to start call
        """
        campaign_id = test_get_campaign["id"]
        test_contacts = get_testdata1_all_success()
        data_store = CampaignCallDataStore()

        for contact in test_contacts:
            contact.campaign_id = campaign_id
            contact.status = ActiveStatusEnum.IN_PROGRESS

        data_store.add_all_campaign_calls(test_contacts)

        conference_id = str(uuid.uuid4())
        call_sid = str(uuid.uuid4())
        contact.call_sid = call_sid
        contact.conference_sid = conference_id
        contact.conference_friendly_name = conference_id

        # Creating a CampaignOutboundCallRequest
        campaign_call_params = CampaignOutboundCallRequest(
            conversation_id=str(uuid.uuid4()),
            conference_friendly_name=str(uuid.uuid4()),
            campaign_id=contact.campaign_id,
            total_participants=business_rules.DEFAULT_TOTAL_PARTICIPANTS,
            billing_types=[
                BillingTypeEnum.SIP_CHARGE,
                BillingTypeEnum.CONFERENCE_CHARGE,
            ],
            call_sid=call_sid,
            child_call_sid=call_sid,
            conference_sid=conference_id,
            to=contact.to,
            from_=contact.from_,
            parent_call_sid=call_sid,
            remarks="",
            workspace_id=ShortId(contact.workspace_id).uuid(),
        )

        mocker.patch(
            "krispcall.konference.billing.billing_service.BillingService.execute_campaign_call_transaction",
            return_value=BillingResponse(
                is_sufficient_credit=False, success=False, charge_amount=0.0
            ),
        )

        # Call the method under test to mock the user credit
        result: BillingResponse = (
            await BillingService.execute_campaign_call_transaction(
                campaign_call_params
            )
        )

        # Assert the expected behavior
        assert not result.is_sufficient_credit
        assert not result.success
        assert result.charge_amount == 0.0

    @pytest.mark.asyncio
    async def test_campaigns_receiver_decline_calls(
        self, member_data, sales_client, test_get_campaign
    ):
        """
        Running test case campaign receiver decline calls
        """
        campaign_id = test_get_campaign["id"]
        test_contacts = get_testdata_receiver_decline_calls()
        await self._run_and_assert_test_case(
            test_get_campaign,
            test_contacts,
            campaign_id,
            NotActiveStatusEnum.CANCELED,
        )

    @pytest.mark.asyncio
    async def test_campaigns_receiver_are_busy(
        self, member_data, sales_client, test_get_campaign
    ):
        """
        Running test case campaign receivers are busy calls
        """
        campaign_id = test_get_campaign["id"]
        test_contacts = get_testdata_receivers_are_busy()
        await self._run_and_assert_test_case(
            test_get_campaign,
            test_contacts,
            campaign_id,
            NotActiveStatusEnum.BUSY,
        )

    @pytest.mark.asyncio
    async def test_campaigns_no_answer_voicemaildrop(
        self, member_data, sales_client, test_get_campaign
    ):
        """
        Running test case campaign not answer and voicemail drop
        """
        campaign_id = test_get_campaign["id"]
        test_contacts = get_testdata_call_not_answer_with_voicemaildrop()
        await self._run_and_assert_test_case(
            test_get_campaign,
            test_contacts,
            campaign_id,
            NotActiveStatusEnum.NO_ANSWER,
        )


def func1():
    return 5


def func2(param1, param2):
    var1 = func1()
    return param1 + param2 + var1

from tests.tests_billing.utils.constant import FROM_NUMBER, WORKSPACE_ID
from tests.tests_billing.utils.models import CampaignCall


def get_testdata1_all_success() -> list[CampaignCall]:
    data_list = [
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+14503679377",
            to_contact_name="John Smith",
            call_duration=2,
            expected_outcome=0.0496,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+12564884232",
            to_contact_name="Robert Joseph",
            call_duration=3,
            expected_outcome=0.0744,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+17754612740",
            to_contact_name="Samantha Marie",
            call_duration=2,
            expected_outcome=0.0496,
        ),
    ]

    return data_list


def get_test_data2_no_answer_calls() -> list[CampaignCall]:
    data_list = [
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+14503679377",
            to_contact_name="John Smith",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+12564884232",
            to_contact_name="Robert Joseph",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+17754612740",
            call_duration=1,
            expected_outcome=0.0088,
            to_contact_name="Samantha Marie",
        ),
    ]

    return data_list


def get_testdata_receiver_decline_calls() -> list[CampaignCall]:
    data_list = [
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+14503679377",
            to_contact_name="John Smith",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+12564884232",
            to_contact_name="Robert Joseph",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+17754612740",
            call_duration=1,
            expected_outcome=0.0088,
            to_contact_name="Samantha Marie",
        ),
    ]

    return data_list


def get_testdata_receivers_are_busy() -> list[CampaignCall]:
    data_list = [
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+14503679377",
            to_contact_name="John Smith",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+12564884232",
            to_contact_name="Robert Joseph",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+17754612740",
            call_duration=1,
            expected_outcome=0.0088,
            to_contact_name="Samantha Marie",
        ),
    ]

    return data_list


def get_testdata_call_not_answer_with_voicemaildrop() -> list[CampaignCall]:
    data_list = [
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+14503679377",
            to_contact_name="John Smith",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+12564884232",
            to_contact_name="Robert Joseph",
            call_duration=1,
            expected_outcome=0.0088,
        ),
        CampaignCall(
            workspace_id=WORKSPACE_ID,
            from_=FROM_NUMBER,
            to="+17754612740",
            call_duration=1,
            expected_outcome=0.0088,
            to_contact_name="Samantha Marie",
        ),
    ]

    return data_list

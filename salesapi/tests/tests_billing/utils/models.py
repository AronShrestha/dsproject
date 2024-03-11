from dataclasses import dataclass, asdict


@dataclass
class CampaignCall:
    workspace_id: str
    from_: str
    to: str
    to_contact_name: str
    call_sid: str = ""
    conference_sid: str = ""
    campaign_id: str = ""
    conference_friendly_name: str = ""
    call_duration: int = 0
    charge_amount: float = 0.0
    running_total_charge: float = 0.0
    elapsed_time: int = 0
    expected_outcome: float = 0
    status: str = ""
    remarks: str = ""


class CampaignCallDataStore:
    def __init__(self):
        self.data_list: list[CampaignCall] = []

    def add_campaign_call(self, campaign_call: CampaignCall):
        self.data_list.append(campaign_call)

    def add_all_campaign_calls(self, campaign_calls: list[CampaignCall]):
        self.data_list.extend(campaign_calls)

    def update(self, contact: CampaignCall):
        for item in self.data_list:
            if contact.to == item.to and contact.from_ == item.from_:
                fields_to_update = {
                    k: v
                    for k, v in asdict(contact).items()
                    if k not in ["from_", "to"]
                }

                # Update the fields
                for field, value in fields_to_update.items():
                    setattr(item, field, value)

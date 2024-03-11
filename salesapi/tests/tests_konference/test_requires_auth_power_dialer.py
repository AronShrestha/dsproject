import pytest
from unittest.mock import AsyncMock, patch
from krispcall.auth.requires_auth_power_dialer import (
    requires_power_dialer_enabled,
)


class TestRequiresPowerDialerEnabled:
    @pytest.mark.asyncio
    async def test_requires_power_dialer_enabled(self):
        # Arrange
        request = AsyncMock()
        request.user.get_claim.return_value = "workspace_id"
        request.context = {"request": request}
        feature_response = {"is_enabled": True}

        # Mock the external dependency
        with patch(
            "krispcall.auth.requires_auth_power_dialer.views.get_workspace_feature",
            return_value=feature_response,
        ):
            # Act:
            decorated_function = requires_power_dialer_enabled(
                self.sample_get_campiagn
            )

            result = await decorated_function(request, AsyncMock())

            # Assert
            assert result == "Success"

    @staticmethod
    async def sample_get_campiagn(_, info):
        return "Success"

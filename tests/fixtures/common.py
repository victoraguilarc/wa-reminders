import pytest

from src.common.domain.context.client import ConsumerClient


@pytest.fixture
def consumer_client() -> ConsumerClient:
    return ConsumerClient.build(
        agent='android:com.collectives.tenant/1.0.0:1',
    )

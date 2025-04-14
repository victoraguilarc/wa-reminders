# -*- coding: utf-8 -*-
from expects import expect, be_a, equal, be_none

from src.common.domain.context.client import ConsumerClient


def test_build_valid_client():
    client = ConsumerClient.build('android:com.package.app/1.0.0-testing:1')

    expect(client).to(be_a(ConsumerClient))
    expect(client.platform).to(equal('android'))
    expect(client.application_id).to(equal('com.package.app'))
    expect(client.version_name).to(equal('1.0.0-testing'))
    expect(client.version_code).to(equal('1'))


def test_build_invalid_client():
    client = ConsumerClient.build('android:com.package.app/1.0.0-testing')

    expect(client).to(be_none)

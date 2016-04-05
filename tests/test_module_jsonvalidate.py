#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_module_jsonencode.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone.event import Event
from wishbone_flow_jsonvalidate import JSONValidate
from wishbone.actor import ActorConfig
from wishbone.utils.test import getter
import os


def test_module_jsonvalidate():

    actor_config = ActorConfig('jsonvalidate', 100, 1, {}, "")

    with open("/tmp/jsonvalidate.jsonschema", "w") as j:
        j.write('{"type": "object", "properties": {"one": { "type": "integer"}}}')

    jsonvalidate = JSONValidate(actor_config, "/tmp/jsonvalidate.jsonschema")

    jsonvalidate.pool.queue.inbox.disableFallThrough()
    jsonvalidate.pool.queue.outbox.disableFallThrough()
    jsonvalidate.pool.queue.failed.disableFallThrough()
    jsonvalidate.start()

    valid = Event({"one": 1})
    invalid = Event({"one": "one"})

    jsonvalidate.pool.queue.inbox.put(valid)
    valid_event = getter(jsonvalidate.pool.queue.outbox)

    jsonvalidate.pool.queue.inbox.put(invalid)
    invalid_event = getter(jsonvalidate.pool.queue.failed)

    os.remove("/tmp/jsonvalidate.jsonschema")

    assert valid_event.get() == {"one": 1}
    assert invalid_event.get() == {"one": "one"}

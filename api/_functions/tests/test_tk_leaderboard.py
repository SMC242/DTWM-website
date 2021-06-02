from unittest import TestCase, TestSuite, TextTestRunner
from asyncio import get_event_loop
from typing import Coroutine
from teamkill_leaderboard import (
    query_factory,
    get_outfit_chars,
    chars_to_ids,
    kill_event_query,
    character_query,
    null_char,
    with_show,
    find_char,
    validate_char_result,
    get_chars_batched,
    char_to_name,
    is_nso,
    find_first_non_nso,
    not_nso_outfit,
    faction_from_char,
    kills_to_factions,
    remove_suicides,
    is_tk,
    count_tks,
    convert_nso,
    check_nso,
    clean_chars,
    do_kill_event_query,
    Faction,
)


class AsyncTest(TestCase):
    def setUp(self):
        self.loop = get_event_loop()

    def run_async(self, coro: Coroutine) -> None:
        """Run an asynchronous test."""
        self.loop.run_until_complete(coro)


class TestQuery(AsyncTest):
    def test_query_factory(self):
        # Check that collections work
        query1 = query_factory("faction")()()
        self.assertEqual(query1.url(
        ), "https://census.daybreakgames.com/get/ps2:v2/faction", "Failed to build collection query")

        # Check that kwargs work
        query2 = query_factory("character")(character_id=1)()
        self.assertEqual(query2.url(
        ), "https://census.daybreakgames.com/get/ps2:v2/character?character_id=1", "Failed to add kwargs to query")

        # Check that joins work
        query3 = query_factory("outfit_member")(outfit_id=1)("character")
        self.assertEqual(query3.url(
        ), "https://census.daybreakgames.com/get/ps2:v2/outfit_member?outfit_id=1&c:join=character",
            "Failed to build join")

    def test_kill_event_query(self):
        kill_event_query
        ...

    def test_character_query(self):
        character_query
        ...

    def test_with_show(self):
        with_show
        ...


class TestChararacters(AsyncTest):

    def test_get_outfit_chars(self):
        get_outfit_chars
        ...

    def test_chars_to_ids(self):
        chars_to_ids
        ...

    def test_null_char(self):
        null_char
        ...

    def test_find_char(self):
        find_char
        ...

    def test_validate_char_result(self):
        validate_char_result
        ...

    def test_get_chars_batched(self):
        get_chars_batched
        ...

    def test_char_to_name(self):
        char_to_name
        ...

    def test_faction(self):
        Faction
        ...

    def test_faction_from_char(self):
        faction_from_char
        ...

    ...


class TestNSO(TestCase):
    def test_is_nso(self):
        is_nso
        ...

    def test_find_first_non_nso(self):
        find_first_non_nso
        ...

    def test_not_nso_outfit(self):
        not_nso_outfit
        ...

    def test_convert_nso(self):
        convert_nso
        ...

    def test_check_nso(self):
        check_nso
        ...

    def test_clean_chars(self):
        clean_chars
        ...

    ...


class TestKills(AsyncTest):
    def test_do_kill_event_query(self):
        do_kill_event_query
        ...

    def test_kills_to_factions(self):
        kills_to_factions
        ...


class TestTKs(TestCase):
    def test_remove_suicides(self):
        remove_suicides
        ...

    def test_is_tk(self):
        is_tk
        ...

    def test_count_tks(self):
        count_tks
        ...


def suite():
    suite = TestSuite()
    suite.addTest(TestQuery())
    suite.addTest(TestChararacters())
    suite.addTest(TestNSO())
    suite.addTest(TestKills())
    suite.addTest(TestTKs())
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())

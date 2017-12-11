# -*- coding: utf-8 -*-
import json
import os
import listenbrainz.db.stats as db_stats
import listenbrainz.db.user as db_user

from listenbrainz.db.testing import DatabaseTestCase


class StatsDatabaseTestCase(DatabaseTestCase):


    def setUp(self):
        DatabaseTestCase.setUp(self)
        self.user = db_user.get_or_create('stats_user')


    def test_insert_user_stats(self):

        with open(self.path_to_data_file('user_top_artists.json')) as f:
            artists = json.load(f)
        with open(self.path_to_data_file('user_top_releases.json')) as f:
            releases = json.load(f)
        with open(self.path_to_data_file('user_top_recordings.json')) as f:
            recordings = json.load(f)


        db_stats.insert_user_stats(
            user_id=self.user['id'],
            artists=artists,
            recordings=recordings,
            releases=releases,
            artist_count=2,
        )

        result = db_stats.get_all_user_stats(user_id=self.user['id'])
        self.assertListEqual(result['artist']['all_time'], artists)
        self.assertEqual(result['artist']['count'], 2)
        self.assertListEqual(result['release']['all_time'], releases)
        self.assertListEqual(result['recording']['all_time'], recordings)
        self.assertGreater(int(result['last_updated'].strftime('%s')), 0)

    def insert_test_data(self):
        """ Insert test data into the database """

        with open(self.path_to_data_file('user_top_artists.json')) as f:
            artists = json.load(f)
        with open(self.path_to_data_file('user_top_releases.json')) as f:
            releases = json.load(f)
        with open(self.path_to_data_file('user_top_recordings.json')) as f:
            recordings = json.load(f)

        db_stats.insert_user_stats(
            user_id=self.user['id'],
            artists=artists,
            recordings=recordings,
            releases=releases,
            artist_count=2,
        )

        return {
            'user_artists': artists,
            'user_releases': releases,
            'user_recordings': recordings,
        }

    def test_get_user_stats(self):
        data_inserted = self.insert_test_data()

        data = db_stats.get_user_stats(self.user['id'], 'artist')
        self.assertEqual(data['artist']['count'], 2)

        data = db_stats.get_user_stats(self.user['id'], 'recording')
        self.assertListEqual(data['recording']['all_time'], data_inserted['user_recordings'])

    def test_get_user_artists(self):
        data_inserted = self.insert_test_data()
        data = db_stats.get_user_artists(self.user['id'])
        self.assertEqual(data['artist']['count'], 2)

    def test_get_all_user_stats(self):
        data_inserted = self.insert_test_data()
        result = db_stats.get_all_user_stats(self.user['id'])
        self.assertListEqual(result['artist']['all_time'], data_inserted['user_artists'])
        self.assertEqual(result['artist']['count'], 2)
        self.assertListEqual(result['release']['all_time'], data_inserted['user_releases'])
        self.assertListEqual(result['recording']['all_time'], data_inserted['user_recordings'])
        self.assertGreater(int(result['last_updated'].strftime('%s')), 0)


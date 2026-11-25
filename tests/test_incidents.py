import tempfile
import unittest
from pathlib import Path
from ashray import database, incidents

class IncidentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_db = database.DB
        database.DB = Path(self.temp.name) / 'test.db'
        database.initialize()
    def tearDown(self):
        database.DB = self.old_db
        self.temp.cleanup()
    def test_english(self):
        i = incidents.submit_report(' Gopalpur ', ' Simulated flood ')
        r = incidents.list_incidents()[0]
        self.assertEqual((r['id'], r['location'], r['report'], r['status']), (i, 'Gopalpur', 'Simulated flood', 'Pending review'))
    def test_odia(self):
        text = 'ଗୋପାଳପୁରରେ ବନ୍ୟା'
        incidents.submit_report('Gopalpur', text)
        self.assertEqual(incidents.list_incidents()[0]['report'], text)
    def test_empty(self):
        for loc, report in [(' ', 'Test'), ('Test', ' ')]:
            with self.assertRaises(ValueError):
                incidents.submit_report(loc, report)
        self.assertEqual(incidents.list_incidents(), [])
    def test_length(self):
        with self.assertRaises(ValueError):
            incidents.submit_report('Gopalpur', 'x'*3001)
    def test_review_and_audit(self):
        i = incidents.submit_report('Gopalpur', 'Simulation')
        incidents.review_incident(i, 'Flooding', 'High')
        r = incidents.list_incidents()[0]
        self.assertEqual((r['category'], r['urgency'], r['status']), ('Flooding','High','Reviewed'))
        self.assertEqual(len(incidents.list_audit()), 2)
    def test_invalid_review(self):
        i = incidents.submit_report('Gopalpur', 'Simulation')
        with self.assertRaises(ValueError):
            incidents.review_incident(i, 'Invalid', 'High')
        with self.assertRaises(ValueError):
            incidents.review_incident(i+1, 'Flooding', 'High')
        self.assertEqual(len(incidents.list_audit()), 1)
    def test_persistence(self):
        incidents.submit_report('Gopalpur', 'First')
        database.initialize()
        incidents.submit_report('Chhatrapur', 'Second')
        self.assertEqual([r['report'] for r in incidents.list_incidents()], ['Second','First'])

if __name__ == '__main__':
    unittest.main()

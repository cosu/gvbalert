import unittest

from gvbalert.tweet import DISTURBANCE, DELAY, DETOUR
from gvbalert.parsing import extract_lines, extract_ride_type, remove_links, extract_event_type, extract_destination, \
    extract_reason


class TestParsing(unittest.TestCase):

    def test_verstoring_druk(self):
        text = 'Verstoring bus 48 en 65 door extreme drukte. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())

        self.assertEquals(['48', '65'], extract_lines(text))
        self.assertEquals('bus', extract_ride_type(text))
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertIsNone(extract_destination(text))
        self.assertEqual('extreme drukte', extract_reason(text))

    def test_verstoring(self):
        text ='Verstoring tram 17 (richting Centraal Station) door een technisch defect. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())
        destination = extract_destination(text)
        self.assertEqual('centraal station', destination)
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertEquals(['17'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    def test_delay(self):
        text = 'Bus 66 rijdt langzaam weer volgens dienstregeling. Houd rekening met vertraging.'
        text = remove_links(text.lower())
        self.assertEquals(DELAY['nl'][0], extract_event_type(text))
        self.assertEquals(['66'], extract_lines(text))
        self.assertEquals('bus', extract_ride_type(text))

    def test_detour(self):
        text = 'Omleiding tram 7 op last van de brandweer vanwege brand op Hoofdweg'
        text = remove_links(text.lower())
        self.assertEquals(DETOUR['nl'][0], extract_event_type(text))
        self.assertEquals(['7'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    def test_delay_tram(self):
        text = 'Tram 7 rijdt geleidelijk weer volgens dienstregeling. Houd rekening met vertraging.'
        text = remove_links(text.lower())
        self.assertTrue(extract_event_type(text) in DELAY['nl'])
        self.assertEquals(['7'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    def test_verstoring_repairs_metro(self):
        text = 'Verstoring metro 51, 53 en 54 door herstelwerkzaamheden. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertEquals(['51', '53', '54'], extract_lines(text))
        self.assertEquals('metro', extract_ride_type(text))
        self.assertEqual('herstelwerkzaamheden', extract_reason(text))

    def test_verstoring_repairs_bus(self):
        text = 'Verstoring bus 22 (richting Station Sloterdijk) door werkzaamheden. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertEquals(['22'], extract_lines(text))
        self.assertEquals('bus', extract_ride_type(text))
        self.assertEqual('werkzaamheden', extract_reason(text))

    def test_running_slowly_tram_2_5(self):
        text = 'Tram 2 en 5 rijdt langzaam weer volgens dienstregeling. Houd rekening met vertraging.'
        text = remove_links(text.lower())
        self.assertEquals(DELAY['nl'][0], extract_event_type(text))
        self.assertEquals(['2', '5'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    def test_running_slowly_2_5_cause(self):
        text = 'Verstoring tram 2 en 5 door een auto op de rails. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertEquals(['2', '5'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))
        self.assertEquals('een auto op de rails', extract_reason(text))

    def test_running_two_destinations(self):
        text = 'Verstoring tram 3 (richting Muiderpoortstation) en 12 (richting Amstelstation) door een technisch defect. Kijk op https://t.co/VtTXVEd4vF'
        text = remove_links(text.lower())
        self.assertEquals(DISTURBANCE['nl'][0], extract_event_type(text))
        self.assertEquals(['3', '12'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    def test_running_slowly_two(self):
        text = 'Tram 9 en 14 rijden langzaam weer volgens dienstregeling. Houd rekening met vertraging.'
        text = remove_links(text.lower())
        self.assertEquals(DELAY['nl'][0], extract_event_type(text))
        self.assertEquals(['9', '14'], extract_lines(text))
        self.assertEquals('tram', extract_ride_type(text))

    @unittest.skip('todo')
    def test_running_slowly(self):
        text = 'Bus 48 en 65 rijden weer volgens dienstregeling.'

    @unittest.skip('todo')
    def test_works_finished(self):
        text = 'Werkzaamheden Prins Hendrikkade eerder klaar dan gepland. Vanaf maandag rijden bus 22, 48 en 248 al weer normale dienstregeling.'

    @unittest.skip('todo')
    def test_repair_normal_time(self):
        text = 'Werkzaamheden Prins Hendrikkade eerder klaar dan gepland. Vanaf maandag rijden bus 22, 48 en 248 al weer normale dienstregeling.'

    @unittest.skip('todo')
    def test_normal_schedule(self):
        text = 'Metro 51, 53 en 54 rijden weer volgens dienstregeling.'

    @unittest.skip('todo')
    def test_increased_delay(self):
        text = 'Oplopende vertraging bus 22 door verkeersdrukte Spaarndammerstraat.'

    @unittest.skip('todo')
    def test_stop_station(self):
        text = 'Bus 22 (richting Station Sloterdijk) halteert weer bij de Oostzaanstraat.'


import csv
import os
import logging
import lxml.etree as et
import datetime
import codecs
import requests
import numpy
import math
import urllib2

global log
logFormat = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(level=logging.WARNING, format=logFormat)
log = logging.getLogger(__name__)

global rubric_path
rubric_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'mrr.csv')


class Belay:
    """Handler for single record analysis"""
    def __init__(self, target, rubric_type):
        log.info('belay initialization')
        self.results = None
        self.target = target
        self.rubric_type = rubric_type
        self.rubric_path = rubric_path
        self.mrr = MasterRubricRulesheet(self)
        self._evaluate_record()
        log.info('belay success! %s', 'http://sylvanrocks.com/images/hero/High-Five-on-Spires.jpg')

    def _evaluate_record(self):
        """Calls RubricV3 class and records results attribute"""
        self.rubric = RubricV3(self, self.target)
        self.results = self.rubric.results

    def master_score(self):
        """Returns master scripts score"""
        return self.rubric.master_score()

    def output_csv(self, output_path):
        """Standard output CSV written to 'output_path'"""
        with codecs.open(output_path, 'w', encoding='utf8') as output:
            header = "Filename, {filename}\n" \
                     "Master Score, {master_score}\n" \
                     "Run Date, {datetime}\n\n\n" \
                     "".format(
                        filename=self.target,
                        master_score=self.rubric.master_score(),
                        datetime=datetime.datetime.now()
                        )
            output.write(header)

            output.write('Element, Rule, Exists, Scored, Rationale, Text, Descent Text, XPath\n')
            for element in self.results.iterkeys():
                e = self.results[element]
                output.write('"%s","%s","%s","%s","%s","%s","%s","%s"\n' %
                             (element, e['rule'], e['exists'], e['scored'],
                              e['log'], e['text'], e['desc_text'], e['xpath']))

    def output_json(self, output_path):
        import json
        output = dict()
        output['recordName'] = self.target.split('/')[-1]
        output['masterScore'] = self.master_score()
        output['dateTime'] = datetime.datetime.isoformat(datetime.datetime.now())
        for key in self.results.iterkeys():
            output[key] = self.results[key]['exists']
        with open(output_path, 'w') as fid:
            fid.write(json.dumps(output, indent=4))


class BelayBatch:
    """Handler for batch record analysis"""
    def __init__(self, target, rubric_type, traverse=False):
        log.info('belay initialization')
        self.target = target
        self.traverse = traverse
        self._check_target()
        self.rubric_type = rubric_type
        self.rubric_path = os.path.join(os.path.dirname(__file__), 'fixtures/mrr.csv')
        self.mrr = MasterRubricRulesheet(self)
        self.summary = dict()
        self.summary_statistics = dict()
        self._evaluate_records()

    def _check_target(self):
        """Confirms that target is a folder for batch processing and returns record path listing"""
        if os.path.isdir(self.target):
            if self.traverse:
                self.directories = list()
                self.records = list()

                self.directories.append(self.target)

                for root_path, directories, files in os.walk(self.target):
                    valid = [x for x in files if x.endswith('.xml')]
                    if directories:
                        for directory in directories:
                            self.directories.append(os.path.join(root_path, directory))
                    if valid:
                        for record in valid:
                            self.records.append(os.path.join(root_path, record))
            else:
                self.records = [self.target + '/' + x for x in os.listdir(self.target) if x.endswith('.xml')]
        else:
            log.error('poorly formed folder target {}'.format(self.target))
            exit(1)

    def _evaluate_records(self):
        """Calls RubricV3 Class on all records in batch and records summary information and statistics"""
        master_scores = list()
        self.summary['records'] = dict()
        for record in self.records:
            rubric = RubricV3(self, record)
            record_summary = {
                'master_score': rubric.master_score(),
                'extra_credit': rubric.extra_credit(),
                'rubric_result': dict(rubric.results)
            }
            self.summary['records'][record.split('/')[-1]] = record_summary
            master_scores.append(rubric.master_score())

        self.summary_statistics = {
            'average_master_score': sum(master_scores)/float(len(master_scores)),
            'above_90': 100*len([x for x in master_scores if x >= 90])/float(len(master_scores)),
            'minimum_score': min(master_scores),
            'maximum_score': max(master_scores),
            'standard_deviation': numpy.std(master_scores),
            'record_count': len(master_scores)
        }
        self.summary['statistics'] = self.summary_statistics

    def output_csv(self, output_path):
        """Standard output CSV written to 'output_path'"""
        with codecs.open(output_path, 'w', encoding='utf8') as output:
            header = "folder, {folder}\n" \
                     "rubric_type, {rubric_type}\n" \
                     "record_count, {record_count}\n" \
                     "average_master_score, {average_master_score}\n" \
                     "above_90, {above_90}\n" \
                     "maximum_score, {maximum_score}\n" \
                     "minumum_score, {minimum_score}\n" \
                     "standard_deviation, {standard_deviation}\n" \
                     "run_datetime, {datetime}\n\n\n"\
                .format(
                    folder=self.target,
                    rubric_type=self.rubric_type,
                    datetime=datetime.datetime.now(),
                    **self.summary['statistics']
                )
            output.write(header)

            element_results = dict()
            for record in self.summary['records'].iterkeys():
                record_element = self.summary['records'][record]
                for element in record_element['rubric_result'].iterkeys():
                    if not element_results.has_key(element):
                        element_results[element] = {
                            'pass': 0,
                            'fail': 0,
                            'ignore': 0
                        }
                    if not record_element['rubric_result'][element]['scored']:
                        element_results[element]['ignore'] += 1
                    else:
                        if record_element['rubric_result'][element]['exists']:
                            element_results[element]['pass'] += 1
                        else:
                            element_results[element]['fail'] += 1

            output.write('element, pass, fail, ignored, xpath\n')
            r = float(len(self.records))
            for element in element_results.iterkeys():
                e = element_results[element]
                output.write('%s, %s, %s, %s, %s\n'
                             % (element,
                                '%0.2f' % (e['pass']),
                                '%0.2f' % (e['fail']),
                                '%0.2f' % (e['ignore']),
                                record_element['rubric_result'][element]['xpath'])
                             )  # counts


class MasterRubricRulesheet:
    """Master scripts rules ingest object"""
    def __init__(self, belay_args):
        log.debug('ingesting scripts rules from :: %s', belay_args.rubric_path)
        mrr_reader = csv.DictReader(open(belay_args.rubric_path))
        self.versions = mrr_reader.next()
        self.rules = dict([(key, [value]) for key, value in mrr_reader.next().iteritems()])
        for row in mrr_reader:
            for key in row.iterkeys():
                self.rules[key].append(row[key])
        for key in self.rules:
            exec 'self.%s = self.rules[key]' % key
        self.iterator = self._get_iterator()

    def _get_iterator(self):
        """Returns iterator for use in content evaluation within RubricV3 class"""
        iterator = list()
        for i in range(len(self.rules['element_id'])):
            iterator.append(dict([(key, self.rules[key][i]) for key in self.rules]))
        return iterator


class RubricV3:
    """Evaluates a single record and returns standard results"""
    def __init__(self, belay_args, record):
        log.debug('evaluating record :: %s', record)
        print("evaluating record %s" % record)
        self.record = record
        self.mrr = belay_args.mrr
        self.rubric_type = belay_args.rubric_type
        self.results = dict()

        self._get_root()
        self._get_content()
        self._parse_rules()
        self._apply_logic()

    def _get_root(self):
        """Grabs XML root"""
        try:
            self.root = et.fromstring(open(self.record).read())
        except IOError as e:
            if self.record.startswith('http'):
                try:
                    self.root = et.fromstring(requests.get(self.record).content)
                except requests.ConnectionError as e:
                    log.error('Invalid HTTP request :: %s', self.record)
                    raise Exception('Invalid HTTP request :: %s' % self.record)
                except BaseException as e:
                    log.error('Invalid Record Path or URL Content')
                    raise Exception('Invalid Record Path or URL Content')
            elif self.record.startswith('ftp'):
                try:
                    request = urllib2.Request(self.record)
                    response = urllib2.urlopen(self.record)
                    content = response.read()
                    self.root = et.fromstring(content)
                except:
                    raise Exception('Invalid FTP')
            else:
                raise ValueError('Invalid Root Path')
        self.map = self.root.nsmap
        if self.map.has_key(None):
            del self.map[None]

    def _get_content(self):
        """Parses element content and assigns to results attribute"""
        for element in self.mrr.iterator:  # iterates over each element as a dictionary from the rules spreadsheet
            error = list()
            id = element['element_id']
            xpath = element['xpath']
            rule = self._get_rule_type(element)

            response = self.root.xpath(xpath, namespaces=self.map)
            count = len(response)
            exists = True if count > 0 else False
            if exists:
                # Extract basic XPath response information (possibly make these subsections RubricV3 methods?)
                if isinstance(response[0], str): # when XPath leads to attribute
                    text = ' || '.join(set(response))
                    attrib = dict([(xpath.split('@')[-1], x) for x in set(response)])
                else:
                    text = ' || '.join(filter(None, [x.text.strip() for x in response if x.text]))
                    text = text if text is not '' else None
                    attrib = filter(None, [x.attrib for x in response])
                    attrib = str(attrib) if attrib else None

                # Retrieve text from all descendants
                if '|' in xpath:
                    xpath_pipes = ' | '.join([x + '/descendant::*/text()' for x in xpath.split(' | ')])
                    desc_text = ' || '.join([x.strip() for x in self.root.xpath(xpath_pipes, namespaces=self.map) if x.strip()])
                else:
                    desc_text = ' || '.join([x.strip() for x in self.root.xpath(xpath + '/descendant::*/text()', namespaces=self.map) if x.strip()])
                desc_text = desc_text if len(desc_text) > 0 else None

                # Check for empty element
                if not any([text, desc_text, attrib]):
                    exists = False
                    error.append('no content in text, desc_text, or attrib')
            else:
                error.append('no element at given xpath')
                text = None
                desc_text = None
                attrib = None

            self.results[id] = {
                'category': element['category'],
                'subcategory': element['subcategory'],
                'rule': rule,
                'if_rule': element['REQUIRED_IF'],
                'if_logic': element['LOGIC'],
                'content_rule': element['content'],
                'or_rule': element['OR'],
                'count': count,
                'xpath': xpath,
                'exists': exists,
                'attrib': attrib,
                'text': text,
                'desc_text': desc_text,
                'log': error,
                'scored': None,  # to be resolved
                'extra_credit': False
                }

    def _apply_logic(self):
        """Handler for logic calls - dependent on scripts type"""
        self._parse_rules()
        self._content_string_check()
        if self.rubric_type in ['collection', 'onestop']:
            self._if_logic_parser()
            self._or_logic_parser()
            self._special_logic_parser()

    def _content_string_check(self):
        """Looks for string match in text or descent text of an ISO element -- adjusts the element exists attribute"""
        for id in self.results.iterkeys():
            if self.results[id]['content_rule']:
                content = self.results[id]['content_rule'].lower()
                all_text = list()
                if self.results[id]['text']:
                    all_text.append(self.results[id]['text'].lower())
                if self.results[id]['desc_text']:
                    all_text.append(self.results[id]['desc_text'].lower())
                if content not in ' '.join(all_text):
                    self.results[id]['exists'] = False
                    self.results[id]['log'].append('failed content check; therefore, exists = false')

    def _if_logic_parser(self):
        """Checks for 'if' dependencies on other elements content and decides if the element will be scored"""
        for id in self.results.iterkeys():
            if self.results[id]['if_rule'] and self.results[id]['rule'] not in ['Recommended', 'Not Required']:
                cases = self.results[id]['if_rule'].split(';')
                if len(cases) < 2:
                    element, logic, value = cases[0].strip().split(' ')
                    if logic == '==':
                        if value in self.results[element]['text'] and self.results[id]['scored'] != False:
                            self.results[id]['scored'] = True
                        else:
                            self.results[id]['scored'] = False
                            self.results[id]['log'].append('not scored because failed if logic parser')
                    elif logic == '!=':
                        if self.results[element]['text'] is None or value not in self.results[element]['text'] and self.results[id]['scored'] != False:
                            self.results[id]['scored'] = True
                        else:
                            self.results[id]['scored'] = False
                            self.results[id]['log'].append('not scored because failed if logic parser')
                else:
                    test = list()
                    for case in cases:
                        element, logic, value = case.strip().split(' ')
                        if logic == '==':
                            test.append(self.results[element]['text'] is not None and value not in self.results[element]['text'])
                        elif logic == '!=':
                            test.append(self.results[element]['text'] is None or value in self.results[element]['text'])
                    if self.results[id]['if_rule'] == 'AND':
                        if all(test):
                            self.results[id]['scored'] = True
                    elif self.results[id]['if_rule'] == 'OR':
                        if not any(test):
                            self.results[id]['logic_failed'] = True

    def _or_logic_parser(self):
        """Checks for 'or' dependencies and decides if the element will be scored"""
        or_groups = dict()
        for id in self.results.iterkeys():
            if self.results[id]['or_rule'] and self.results[id]['scored'] != False:
                if or_groups.has_key(self.results[id]['or_rule']):
                    or_groups[self.results[id]['or_rule']].append(id)
                else:
                    or_groups[self.results[id]['or_rule']] = [id]
        for group in or_groups:
            found = False
            for element in or_groups[group]:
                if not found and self.results[element]['exists']:
                    self.results[element]['scored'] = True
                else:
                    self.results[element]['scored'] = False
                    self.results[element]['log'].append('not scored because or rule parser')
            if not found:
                self.results[or_groups[group][0]]['scored'] = True
                for element in or_groups[group][1:]:
                    self.results[element]['scored'] = False
                    if 'not scored because or rule parser' not in self.results[element]['log']:
                        self.results[element]['log'].append('not scored because or rule parser')

    def _special_logic_parser(self):
        """Special logic that would be too cumbersome to dynamically enact -- decides if element will be scored"""
        groups = dict()  #  content category
        groups['features'] = {
            'elements': ['featureCatalogCitation', 'featureCatalogIncluded', 'featureTypes', 'featureCatalogURL']}
        groups['attributes'] = {
            'elements': ['coverageAttributeType', 'coverageRange', 'coverageDimension', 'coverageDetails',
                         'coverageAttribute']}
        for subcategory in groups.iterkeys():
            subcategory_score = 0
            for element in groups[subcategory]['elements']:
                if self.results[element]['rule'] == 'Required' and self.results[element]['exists']:
                    subcategory_score += 1
                groups[subcategory]['score'] = subcategory_score
        if groups['features']['score'] >= groups['attributes']['score']:
            for element in groups['features']['elements']:
                if self.results[element]['rule'] not in ['Recommended', 'Not Required']:
                    self.results[element]['scored'] = True
                    self.results[element]['log'].append(
                        'features subcategory scored because passed special logic parser')
            for element in groups['attributes']['elements']:
                self.results[element]['scored'] = False
                self.results[element]['log'].append(
                    'attributes subcategory not scored because failed special logic parser (features elements scored) '
                    '- now extra credit')
                self.results[element]['extra_credit'] = True
        else:
            for element in groups['attributes']['elements']:
                if self.results[element]['rule'] not in ['Recommended', 'Not Required']:
                    self.results[element]['scored'] = True
                    self.results[element]['log'].append(
                        'attributes subcategory scored because passed special logic parser')
            for element in groups['features']['elements']:
                self.results[element]['scored'] = False
                self.results[element]['log'].append(
                    'features subcategory not scored because failed special logic parser (attributes elements scored) '
                    '- now extra credit')
                self.results[element]['extra_credit'] = True

        groups = dict()
        groups['lineage'] = {'elements':
                                 ['lineageScope', 'source', 'processStep', 'processor']}
        groups['acquisition'] = {'elements':
                                     ['platformID', 'platformDescription', 'instrumentID',
                                      'instrumentDescription', 'platformKeyword', 'platformKeywordThesaurus',
                                      'instrumentKeyword', 'instrumentKeywordThesaurus']}
        for subcategory in groups.iterkeys():
            subcategory_score = 0
            for element in groups[subcategory]['elements']:
                if self.results[element]['rule'] == 'Required' and self.results[element]['exists']:
                    subcategory_score += 1
                groups[subcategory]['score'] = subcategory_score
        if groups['lineage']['score'] >= groups['acquisition']['score']:
            for element in groups['lineage']['elements']:
                if not self.results[element]['extra_credit']:
                    self.results[element]['scored'] = True # add rationale to special logic to make result more clear
                    self.results[element]['log'].append(
                        'lineage subcategory scored because passed special logic parser')
            for element in groups['acquisition']['elements']:
                self.results[element]['scored'] = False
                self.results[element]['log'].append(
                    'aquisition subcategory not scored because failed special logic parser (lineage elements scored) - '
                    'now extra credit')
                self.results[element]['extra_credit'] = True
        else:
            for element in groups['acquisition']['elements']:
                if not self.results[element]['extra_credit']:
                    self.results[element]['scored'] = True
                    self.results[element]['log'].append(
                        'acquisition subcategory scored because passed special logic parser')
            for element in groups['lineage']['elements']:
                self.results[element]['scored'] = False
                self.results[element]['log'].append(
                    'lineage subcategory not scored because failed special logic parser (aquisition elements scored) - '
                    'now extra credit')
                self.results[element]['extra_credit'] = True

        if groups['acquisition']['score'] == 0 and groups['lineage']['score'] == 0:
            self.results['lineageStatement']['scored'] = False # True
            self.results[element]['log'].append('lineageStatement scored because passed special logic parser')
        else:
            self.results['lineageStatement']['scored'] = False
            self.results[element]['log'].append('not scored because failed special logic parser')

    def _get_rule_type(self, element):
        """Assigns correct rules from MasterRubricRulesheet to results rules attribute"""
        if self.rubric_type == 'granule':
            rule = element['granule_rules']
        elif self.rubric_type == 'collection':
            rule = element['collection_rules']
        # elif self.rubric_type == 'onestop':
        #     rule = element['onestop_rules']
        else:
            raise Exception("invalid rubric type ({}): valid types - 'collection', 'granule'".format(self.rubric_type))
        return rule

    def _parse_rules(self):
        """Sets pre-logic values for scored attribute for each element"""
        for id in self.results.iterkeys():
            if self.results[id]['rule'] in ['Required', 'Conditional']:
                self.results[id]['scored'] = True
            else:
                self.results[id]['scored'] = False
            if self.results[id]['rule'] == 'Recommended':
                self.results[id]['extra_credit'] = True

    def master_score(self):
        """Returns master scripts score for the record"""
        passed = 0
        scored = 0
        for id in sorted(self.results.iterkeys()):
            if self.results[id]['scored']:
                scored += 1
                if self.results[id]['exists']:
                    passed += 1
        return int(math.ceil(100*float(passed)/scored))

    def extra_credit(self):
        """Returns extra credit score for the record"""
        extra_credit = 0
        for id in self.results.iterkeys():
            if self.results[id]['extra_credit'] and self.results[id]['exists']:
                extra_credit += 1
        return extra_credit

    def to_json(self):
        for key in self.results.iterkeys():
            print key


def Evaluate(target, rubric_type='collection', traverse=False):
    """Main call function, determines if request is single record or batch and returns approptiate belay class
    instance"""
    if os.path.isfile(target):
        log.info('valid target record: %s', target)
        result = Belay(target, rubric_type)
    elif os.path.isdir(target):
        log.info('valid target folder: %s', target)
        if len([x for x in os.listdir(target) if x.endswith('.xml')]) > 0:
            result = BelayBatch(target, rubric_type, traverse=traverse)
        else:
            log.warning('no valid records in target folder: %s', target)
            result = None
    elif target.startswith('http'):
        log.info('URL target record: %s', target)
        result = Belay(target, rubric_type)
    elif target.startswith('ftp'):
        log.info('FTP target record: %s', target)
        result = Belay(target, rubric_type)
    else:
        log.error('invalid target: %s', target)
        result = None
    return result


if __name__ == '__main__':
    # b = Evaluate('ftp://ftp.nodc.noaa.gov/pub/outgoing/Li/metadata/FNCM_201010_5508V1.nc.xml', 'granule')
    # print b.target
    # print b.results.keys()
    # print b.master_score()
    # b.output_csv('blah.csv')
    # report = Evaluate('https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.nodc:0114815;view=xml')
    # import json
    # print json.dumps(report.results['coverageDetails'], indent=2)
    report = BelayBatch('/nodc/projects/satdata/Granule_OneStop/WOA13/xml', rubric_type='granule', traverse=True)
    report.output_csv('rubric_scores.csv')
    # print len(report.records)
    # for record in report.records:
    #     print record
    # record = Evaluate('https://www.ngdc.noaa.gov/metadata/published/NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/5490.xml', 'collection')
    # print record.master_score()
    # folder = 'fixtures/samples'
    # for filename in [os.path.join(folder, x) for x in os.listdir(folder) if x.endswith('.xml')]:
    #     record = Evaluate(filename, 'collection')
    #     record.output_json(os.path.join('/Users/arosenbe/Elasticsearch/records', record.target.split('/')[-1]) + '.json')

    # import json
    # print json.dumps(record.results, indent=4)
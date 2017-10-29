"""@ingroup vigilence
@file
Contains glue that relates all vigilence concepts together into "quality suites".
These suites can be added by users as plugins and selected via the command line.
"""
from vigilence.configuration import ConfigurationParser
from vigilence.constraint import ConstraintSuite
from vigilence.error import QualityViolationsDetected

class QualitySuite(object):
    """Represents a full set of quality metrics that should be enforced upon a codebase.
    The QualitySuite consists of a combination of the lower-level vigilence concepts:
    1. Metrics: the raw data points that comprise the quality check
    2. Quality items: the individual unit for which metrics are collected (e.g. files, modules, classes, functions, etc.)
    3. Parsers: the translators that turn raw metrics into vigilence-compatible quality items.
    4. Constraints: the requirements for the metrics collected for the various quality items in the codebase.
    5. Configuration stanzas: the configurations necessary for a user to model all of the above in a simple configuration file.
    """
    Suites = {}
    def __init__(self, parser, constraints, configurations):
        self.reportParser = parser
        self.constraints = ConstraintSuite(constraints)
        stanzas = {key: config(self.constraints) for key, config in configurations.iteritems()}
        self.configurationParser = ConfigurationParser(stanzas, self.constraints)

    def run(self, configuration, report):
        """Runs the quality suite with the provided configuration on the provided quality report.
        @param configuration The string contents of the vigilence configuration file.
        @param report The string contents of the quality report.
        @throws vigilence.error.QualityViolationsDetected
        """
        constraints = self.configurationParser.parse(configuration)
        quality = self.reportParser.parse(report)
        dissatisfactions = quality.scrutinize(constraints)
        for failure in dissatisfactions:
            print failure.message
        if dissatisfactions:
            raise QualityViolationsDetected('One or more quality violations detected')
        print 'Quality validation complete'

    @classmethod
    def add_suite(cls, key, parser, constraints, configurations):
        """Adds a quality suite to the vigilence registry.
        This suite will be available via the vigilence command line utility.
        @param cls
        @param key The string identifier that should be used to access the quality suite.
        @param parser A vigilence.parser.Parser instance.
        @param constraints A dictionary mapping constraint labels to their corresponding class objects.
        @param configurations A dictionary mapping configuration keys to the corresponding class objects.
        @throws ValueError if @p key is already in use.
        @see vigilence.configuration.ConfigurationStanza
        @see vigilence.constraint.Constraint
        """
        if key in cls.Suites:
            raise ValueError('Quality suite "{}" already exists'.format(key))
        cls.Suites[key] = QualitySuite(parser, constraints, configurations)

    @classmethod
    def available_suites(cls):
        """Returns a list of all available quality suite names.
        """
        return cls.Suites.keys()

    @classmethod
    def get_suite(cls, key):
        """Returns the QualitySuite associated with @p key.
        """
        return cls.Suites[key]

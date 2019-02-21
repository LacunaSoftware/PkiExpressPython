from .validation_results import ValidationResults
from .cades_timestamp import CadesTimestamp
from .digest_algorithm_and_value import DigestAlgorithmAndValue
from .signature_algorithm_and_value import SignatureAlgorithmAndValue
from .signature_policy_identifier import SignaturePolicyIdentifier
from .pk_certificate import PKCertificate


class CadesSignerInfo(object):

    def __init__(self, model):
        self.__signing_time = model.get('signingTime', None)
        self.__certified_date_reference = \
            model.get('certifiedDateReference', None)

        self.__message_digest = None
        message_digest = model.get('messageDigest', None)
        if message_digest is not None:
            self.__message_digest = DigestAlgorithmAndValue(message_digest)

        self.__signature = None
        signature = model.get('signature', None)
        if signature is not None:
            self.__signature = SignatureAlgorithmAndValue(signature)

        self.__certificate = None
        certificate = model.get('certificate', None)
        if certificate is not None:
            self.__certificate = PKCertificate(certificate)

        self.__signature_policy = None
        signature_policy = model.get('signaturePolicy', None)
        if signature_policy is not None:
            self.__signature_policy = SignaturePolicyIdentifier(signature_policy)

        self.__timestamps = []
        timestamps = model.get('timestamps', None)
        if timestamps is not None:
            for timestamp in timestamps:
                self.__timestamps.append(CadesTimestamp(timestamp))

        self.__validation_results = None
        validation_results = model.get('validationResults', None)
        if validation_results is not None:
            self.__validation_results = ValidationResults(validation_results)

    @property
    def signing_time(self):
        return self.__signing_time

    @signing_time.setter
    def signing_time(self, value):
        self.__signing_time = value

    @property
    def certified_date_reference(self):
        return self.__certified_date_reference

    @certified_date_reference.setter
    def certified_date_reference(self, value):
        self.__certified_date_reference = value

    @property
    def message_digest(self):
        return self.__message_digest

    @message_digest.setter
    def message_digest(self, value):
        self.__message_digest = value

    @property
    def signature(self):
        return self.__signature

    @signature.setter
    def signature(self, value):
        self.__signature = value

    @property
    def certificate(self):
        return self.__certificate

    @certificate.setter
    def certificate(self, value):
        self.__certificate = value

    @property
    def signature_policy(self):
        return self.__signature_policy

    @signature_policy.setter
    def signature_policy(self, value):
        self.__signature_policy = value

    @property
    def timestamps(self):
        return self.__timestamps

    @timestamps.setter
    def timestamps(self, value):
        self.__timestamps = value

    @property
    def validation_results(self):
        return self.__validation_results

    @validation_results.setter
    def validation_results(self, value):
        self.__validation_results = value


__all__ = ['CadesSignerInfo']

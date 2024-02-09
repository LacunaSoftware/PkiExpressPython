import base64
import os
import uuid
import pytest
import requests
from pkiexpress import standard_signature_policies
from pkiexpress.authentication import Authentication
from pkiexpress.cades_signature_editor import CadesSignatureEditor
from pkiexpress.cades_signature_explorer import CadesSignatureExplorer
from pkiexpress.cades_signature_starter import CadesSignatureStarter
from pkiexpress.pades_signature_explorer import PadesSignatureExplorer
from pkiexpress.pades_signature_starter import PadesSignatureStarter
from pkiexpress.pki_express_config import PkiExpressConfig
from pkiexpress.signature_finisher import SignatureFinisher
from pkiexpress.timestamp_authority import TimestampAuthority
from pkiexpress import DigestAlgorithms

""" This test class includes smoke tests using PKI Express client lib and a local server which performs the signatures
    The test cases are:
        * Authentication
        * PAdES Signature
        * PAdES Document validation
        * CAdES Signature
        * CAdES Document validation
        * CAdES Document Merge 

"""
class PkiExpressSmokeTests():
    REST_PKI_ACCESS_TOKEN = None
    config = PkiExpressConfig(
            pki_express_home = None,
            temp_folder = None,
            transfer_data_folder = None
    )
    certificate_base64 = "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"
    server_url = "http://localhost:5128/"
    print(os.path.join(os.getcwd(), "00.pdf"))
    pdf_to_sign = os.path.join(os.getcwd(), "00.pdf")
    signed_pdf = os.path.join(os.getcwd(), "00_signed.pdf")
    signed_p7s = os.path.join(os.getcwd(), "00_signed.p7s")
    cades_pdf_extracted_path = os.path.join(os.getcwd(), "cades_pdfs_extracted\\")
    cades_merge_results_path = cades_pdf_extracted_path + "merge_results\\"

    # CMS files
    cms_data_file = os.path.join(os.getcwd(), "CMSDataFile.pdf")
    cms_attached_1 = os.path.join(os.getcwd(), "CMSAttached1.p7s")
    cms_attached_2 = os.path.join(os.getcwd(), "CMSAttached2.p7s")
    cms_detached_1 = os.path.join(os.getcwd(), "CMSDetached1.p7s")
    cms_detached_2 = os.path.join(os.getcwd(), "CMSDetached2.p7s")
    

    """ Text fixture, add all configs to self.config """
    def set_pki_defaults(self, operator):
        trusted_roots = []
        for root in trusted_roots:
            operator.add_trusted_root(root)

        # Set the operator to "OFFLINE MODE" (default: false):
        operator.offline = False
        # Set the operator to use a timestamp authority when performing an timestamp
        # operation. In this sample, we will use the REST PKI by default to emit a
        # timestamp. It only be filled if the REST PKI token was provided.
        if self.REST_PKI_ACCESS_TOKEN is not None:

            # Get an instance of the TimestampAuthority class, responsible to inform
            # the URL and authentication parameters to be used when contacting the
            # timestamp authority.
            authority = TimestampAuthority('https://pki.rest/tsp/a402df41-8559-47b2-a05c-be555bf66310')

            # Set authentication strategy. In the case of REST PKI, is using a
            # bearer token.
            authority.set_oauth_token_authentication(self.REST_PKI_ACCESS_TOKEN)

            # Add authority to be used on operator.
            operator.timestamp_authority = authority

        # Trust Lacuna Test Root (for development purposes only!). Use this to
        # accept the test certificate provided by Lacuna Software.
        operator.trust_lacuna_test_root = True
        
        # THIS SHOULD NEVER BE USED ON PRODUCTION ENVIRONMENT!
        # you may change these configurations to your liking

    def perform_authentication(self):
        auth = Authentication(self.config)
        auth.trust_lacuna_test_root = True
        auth.certificate_base64 = self.certificate_base64
        res = auth.start()
        assert res.nonce != ""
        assert self.is_in_digest_algorithm(res.digest_algorithm.replace('-', ""))
        assert res.digest_algorithm_oid != ""
        auth_params = [{"toSignHash": res.nonce}, {"digestAlgorithm": res.digest_algorithm}, {"op": "2"}]
        # Perform HTTP request
        auth_start_res = self.perform_http_sign(auth_params)
        # Now we'll finish the authentication by sending the signed nonce to the API
        # Set PKI default options (see utils.py).
        # Set the nonce. This value is generate on "start" action
        auth.certificate_base64 = self.certificate_base64
        auth.nonce_base64 = res.nonce
        # Set the Base64-encoded certificate content.
        auth.signature_base64 = auth_start_res.text
        res = auth.complete()
        assert res.validation_results.is_valid == True
        assert res.certificate is not None
    
    """ Second test case: PAdES signature """
    def perform_pades_signature(self):
        signature_starter = PadesSignatureStarter(config=self.config)
        # Set signature policy.
        signature_starter.signature_policy = standard_signature_policies.PADES_BASIC
        # Set PDF to be signed
        signature_starter.set_pdf_to_sign_from_path(self.pdf_to_sign)
        # Set Base64-encoded certificate's content to signature starter.
        signature_starter.set_certificate_from_base64(self.certificate_base64)
        start_res = signature_starter.start()
        assert start_res['toSignHash'] != ""
        assert start_res['transferFile'] != ""
        assert start_res['digestAlgorithm'] != ""
        # Since we're not performing the signature with WebPki as this 
        # would require further dependencies to be installed alongside the library
        # We'll use a local service which mimics the webPki function and signs the 
        # hash sent by the start() function
        sign_params = [{"toSignHash": start_res["toSignHash"]}, {"digestAlgorithm": start_res["digestAlgorithm"]}, {"op": "1"}]
        # Perform HTTP request
        signature = self.perform_http_sign(params=sign_params)
        # Now we move on to finish the pades signature
        signature_finisher = SignatureFinisher(self.config)
        self.set_pki_defaults(signature_finisher)
        signature_finisher.set_file_to_sign_from_path(self.pdf_to_sign)
        signature_finisher.set_transfer_file_from_path(start_res["transferFile"])
        signature_finisher.signature = signature.content
        signature_finisher.output_file  = self.create_file(self.signed_pdf)
        signer_cert = signature_finisher.complete(get_cert=True)
        assert signer_cert is not None
        assert signer_cert.pki_brazil.responsavel == "Alan Mathison Turing"
    
    def perform_validate_pades(self):
        # Get an instance of the PadesSignatureExplorer class, used to open/validate
        # PDF signatures.
        sig_explorer = PadesSignatureExplorer()
        # Set PKI default options (see utils.py)
        self.set_pki_defaults(sig_explorer)
        # Specify that we want to validate the signatures in the file, not only
        # inspect them.
        sig_explorer.validate = True
        # Set the PDF file to be inspected.
        sig_explorer.set_signature_file_from_path(self.signed_pdf)
        # Call the open() method, which returns the signature file's information.
        signature = sig_explorer.open()
        assert len(signature.signers) != 0
        assert signature.signers[0].certificate.subject_name.common_name == "Alan Mathison Turing"

    def perform_cades_signature(self):
        # Get an instance of the CadesSignatureStarter class, responsible for
        # receiving the signature elements and start the signature process.
        signature_starter = CadesSignatureStarter()
        # Set PKI default options (see utils.py).
        self.set_pki_defaults(signature_starter)
        # Set signature policy.
        signature_starter.signature_policy = \
            standard_signature_policies.PKI_BRAZIL_CADES_ADR_BASICA
        # Set file to be signed. If the file is a CMS, PKI Express will
        # recognize that and will co-sign that file.
        signature_starter.set_file_to_sign_from_path(self.pdf_to_sign)
        # Set Base64-encoded certificate's content to signature starter.
        signature_starter.set_certificate_from_base64(self.certificate_base64)
        # Set 'encapsulated content' option (default: True).
        signature_starter.encapsulated_content = True
        # Start the signature process. Receive as response the following fields:
        # - to_sign_hash:     The hash to be signed.
        # - digest_algorithm: The digest algorithm that will inform the Web PKI
        #                     component to compute the signature.
        # - transfer_file:    A temporary file to be passed to "complete" step.
        start_res = signature_starter.start()
        # Perform HTTP Request
        sign_params = [{"toSignHash": start_res["toSignHash"]}, {"digestAlgorithm": start_res["digestAlgorithm"]}, {"op": "1"}]
        signature = self.perform_http_sign(sign_params)
        # Now we move on to finish the cades signature
        signature_finisher = SignatureFinisher(self.config)
        signature_finisher.trust_lacuna_test_root = True
        signature_finisher.set_file_to_sign_from_path(self.pdf_to_sign)
        signature_finisher.set_transfer_file_from_path(start_res["transferFile"])
        signature_finisher.signature = signature.content
        signature_finisher.output_file  = self.create_file(self.signed_p7s)
        signer_cert = signature_finisher.complete(get_cert=True)
        assert signature_finisher.output_file is not None
        assert signer_cert is not None
        assert signer_cert.pki_brazil.responsavel == "Alan Mathison Turing"

    def perform_validate_cades(self):
        # Get an instance of the PadesSignatureExplorer class, used to open/validate
        # PDF signatures.
        sig_explorer = CadesSignatureExplorer()
        # Set PKI default options (see utils.py)
        self.set_pki_defaults(sig_explorer)
        # Specify that we want to validate the signatures in the file, not only
        # inspect them.
        sig_explorer.validate = True
        # Set the PDF file to be inspected.
        sig_explorer.set_signature_file_from_path(self.signed_p7s)
        output_file = self.cades_pdf_extracted_path + '%s.pdf' % (str(uuid.uuid4()))
        output_file = self.create_file(output_file)
        sig_explorer.extract_content_path = output_file
        # Call the open() method, which returns the signature file's information.
        signature = sig_explorer.open()
        assert len(signature.signers) != 0
        assert signature.signers[0].certificate.subject_name.common_name == "Alan Mathison Turing"

    def perform_merge_cades(self):
        # Get an instance of the CadesSignatureEditor class, responsible for
        # receiving the files and merge them.
        signature_editor = CadesSignatureEditor()
        # Set PKI default options (see utils.py).
        self.set_pki_defaults(signature_editor)
        # Generate output filename
        output_file = '%s.p7s' % (str(uuid.uuid4()))
        # Set the CMS data file
        signature_editor.set_data_file_from_path(self.cms_data_file)
        # Add both signatures
        signature_editor.add_cms_file_from_path(self.cms_attached_1)
        signature_editor.add_cms_file_from_path(self.cms_attached_2)
        # Set path to output file
        output_file =  self.create_file(self.cades_merge_results_path + '%s.p7s' % (str(uuid.uuid4())))
        signature_editor.output_file = output_file
        # Merge files
        signature_editor.merge()
        assert len(signature_editor.output_file) != 0

    """ Performs HTTP request to local service which signs data using Alan Turing's test certificate """
    def perform_http_sign(self, params):
        url = self.server_url+"WebPki"
        req_params =  {key: value for param_object in params for key, value in param_object.items()}
        # Perform the POST request
        signature = requests.post(url, params=req_params)
        return signature

    def run_tests(self):
        # Authentication
        self.perform_authentication()
        # PAdES test suites
        self.perform_pades_signature()
        self.perform_validate_pades()
        # CAdES test suites
        self.perform_cades_signature()
        self.perform_validate_cades()
        self.perform_merge_cades()
    
    def is_in_digest_algorithm(self, digest_algorithm: str):
        if digest_algorithm in dir(DigestAlgorithms):
            return True
        else:
            return False

    def create_file(self, file_path: str):
        try:
            # Try to open the file in read mode to check if it exists
            with open(file_path, 'r'):
                pass  # File exists, do nothing
        except FileNotFoundError:
            # File does not exist, create it
            with open(file_path, 'w') as file:
                file.write("This is a new file.")
        return file_path


test_class = PkiExpressSmokeTests()
test_class.run_tests()
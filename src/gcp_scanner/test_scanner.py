import unittest
import scanner
from unittest.mock import MagicMock

class TestScanner(unittest.TestCase):
    
    def test_scan_single_resource_with_valid_input(self):
        # Test with a valid GCP resource that should return findings
        resource = {'type': 'gcp-type', 'id': 'gcp-resource-id'}
        findings = scan_single_resource(resource)
        self.assertIsNotNone(findings)
        
    def test_scan_single_resource_with_invalid_input(self):
        # Test with an invalid GCP resource that should return None
        resource = {'type': 'invalid-type', 'id': 'invalid-id'}
        findings = scan_single_resource(resource)
        self.assertIsNone(findings)
    
    def test_get_resources(self):
        # Test that get_resources returns a list of resources
        resources = get_resources("project_id")
        self.assertIsInstance(resources, list)

        # Test that each resource is a string
        for resource in resources:
            self.assertIsInstance(resource, str)

    def test_get_all_resources(self):
        # Test that get_all_resources returns a list of resources
        resources = get_all_resources()
        self.assertIsInstance(resources, list)

        # Test that each resource is a string
        for resource in resources:
            self.assertIsInstance(resource, str)
    
    def test_scan_project(self):
        project = {'project_id': 'test-project'}
        credentials = MagicMock()
        credentials.project_id.return_value = 'test-project'
        resources = [{'type': 'google_compute_instance', 'id': 'instance-1'},
                     {'type': 'google_storage_bucket', 'id': 'bucket-1'}]
        scanner = MagicMock()
        scanner.scan_single_resource.side_effect = [{'resource': 'instance-1', 'vulnerabilities': []},
                                                    {'resource': 'bucket-1', 'vulnerabilities': []}]
        expected_result = {'project_id': 'test-project', 'resources': [{'resource': 'instance-1', 'vulnerabilities': []},
                                                                       {'resource': 'bucket-1', 'vulnerabilities': []}]}

        result = scan_project(project, credentials, scanner)

        self.assertEqual(result, expected_result)

    def test_scan_projects(self):
        # Test that scan_projects function scans GCP resources in parallel
        credentials, projects = scanner.load_projects('test_projects.json')
        results = scanner.scan_projects(projects, credentials, concurrency=5)
        self.assertEqual(len(results), len(projects))

    def test_main(self):
        # Test that main function correctly sets the concurrency level using command-line argument
        args = '--project_file test_projects.json --concurrency 3'.split()
        scanner.main(args)
        with open('results.json') as f:
            results = f.readlines()
        self.assertEqual(len(results), 3)  
       
        
    

if __name__ == '__main__':
    unittest.main()

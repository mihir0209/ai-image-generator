import boto3
from datetime import datetime
import traceback
from config import Config

class CloudWatchHelper:
    def __init__(self):
        try:
            if Config.USE_IAM_ROLE:
                # Use IAM role when on EC2
                self.cloudwatch = boto3.client('cloudwatch', region_name=Config.AWS_REGION)
            else:
                # Use credentials from environment
                self.cloudwatch = boto3.client('cloudwatch', region_name=Config.AWS_REGION)
            
            self.namespace = Config.CLOUDWATCH_NAMESPACE
            print(f"CloudWatch client initialized. Namespace: {self.namespace}")
        except Exception as e:
            print(f"Failed to initialize CloudWatch client: {str(e)}")
            self.cloudwatch = None
    
    def put_metric(self, metric_name, value, unit='Count', dimensions=None):
        """Send custom metric to CloudWatch"""
        if not self.cloudwatch:
            return False
        
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
            
            if dimensions:
                metric_data['Dimensions'] = dimensions
            
            response = self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[metric_data]
            )
            
            print(f"Metric sent: {metric_name} = {value}")
            return True
        except Exception as e:
            print(f"Error sending metric: {str(e)}")
            return False
    
    def increment_counter(self, metric_name, dimensions=None):
        """Increment a counter metric"""
        return self.put_metric(metric_name, 1, 'Count', dimensions)
    
    def record_time(self, metric_name, milliseconds, dimensions=None):
        """Record a timing metric"""
        return self.put_metric(metric_name, milliseconds, 'Milliseconds', dimensions)
    
    def record_generation(self, success=True, model=None):
        """Record image generation event"""
        dimensions = [{'Name': 'Status', 'Value': 'Success' if success else 'Failed'}]
        if model:
            dimensions.append({'Name': 'Model', 'Value': model})
        
        return self.increment_counter('ImageGenerations', dimensions)
    
    def record_user_registration(self):
        """Record new user registration"""
        return self.increment_counter('UserRegistrations')
    
    def record_login(self):
        """Record user login"""
        return self.increment_counter('UserLogins')
    
    def record_error(self, error_type='General'):
        """Record application error"""
        dimensions = [{'Name': 'ErrorType', 'Value': error_type}]
        return self.increment_counter('ApplicationErrors', dimensions)

# Global instance
cloudwatch = CloudWatchHelper()

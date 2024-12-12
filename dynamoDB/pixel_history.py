import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class PixelHistory:
    """
    Example data structure:
    {
        "pixel": "400 400",
        "date_time": "2024-12-05T14:15:30Z",
        "rgb": "50 25 20"
    }
    """

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        # The table variable is set during the scenario in the call to
        # 'exists' if the table exists. Otherwise, it is set by 'create_table'.
        self.table = None


    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        else:
            self.table = table
        return exists
    
    
    def add_pixels(self, lst):
        """
        Add pixels to the history table.
        """
        try:
            with self.table.batch_writer() as batch:
                for i in lst:
                    batch.put_item(
                        Item={
                            "pixel": i['pixel'],
                            "date_time": i['t'],
                            "rgb": i['rgb']
                        }
                    )
        except ClientError as err:
            logger.error(
                "Couldn't add pixels to table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        

    def get_pixels(self):
        """
        Gets pixel history from the history table.
        """
        try:
            response = self.table.scan()
        except ClientError as err:
            logger.error(
                "Couldn't get pixels from table %s. Here's why: %s: %s",
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Item"]
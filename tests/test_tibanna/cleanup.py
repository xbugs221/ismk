import subprocess
import boto3

# clean up local
subprocess.call(["rm", "-rf", ".ismk"])
subprocess.call(["rm", "-rf", "ismk-tibanna-test"])

# clean up s3
s3 = boto3.client("s3")
s3.delete_objects(
    Bucket="ismk-tibanna-test",
    Delete={
        "Objects": [
            {"Key": "1/message1"},
            {"Key": "1/message2"},
            {"Key": "1/next_message"},
            {"Key": "1/final_message"},
        ]
    },
)
s3.delete_objects(
    Bucket="ismk-tibanna-test2", Delete={"Objects": [{"Key": "1/final_message"}]}
)

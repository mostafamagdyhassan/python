

import pymysql
import boto3

# AWS RDS DB credentials
host = "your-rds-endpoint.amazonaws.com"
user = "your_db_username"
password = "your_db_password"
database = "your_db_name"
port = 3306  # MySQL default port

# User ID to search for
user_id = 1234

try:
    # Connect to RDS MySQL
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
    )

    with connection.cursor() as cursor:
        # Query to get email, name, date_of_completion by user ID
        sql_query = """
            SELECT email, name, date_of_completion 
            FROM users 
            WHERE id = %s
        """
        cursor.execute(sql_query, (user_id,))
        
        # Fetch results into list of dicts
        results = cursor.fetchall()

    # Save data into a Python list for later use
    user_data_list = []
    for row in results:
        user_data_list.append({
            'email': row['email'],
            'name': row['name'],
            'date_of_completion': row['date_of_completion']
        })

    print("Retrieved User Data:", user_data_list)

except Exception as e:
    print("Error:", e)

finally:
    if 'connection' in locals():
        connection.close()
      
# Create an SES client
ses_client = boto3.client('ses', region_name='us-east-1')  # Change region if needed

# Sender and recipient details
sender_email = "your_verified_email@example.com"  # Must be verified in SES (sandbox mode)
subject = "Congratulations on Completing Your Task"

# Assume this is the user data from the list you created
user_data_list = [{
    'email': 'recipient@example.com',
    'name': 'John Doe',
    'date_of_completion': '2025-07-10'
}]

# Loop over each user and send email
for user in user_data_list:
    recipient_email = user['email']
    name = user['name']
    date = user['date_of_completion']

    # Email body (plain text and HTML)
    body_text = f"""Hello {name},

Congratulations on completing your task on {date}!

Best regards,
Your Team"""

    body_html = f"""
    <html>
    <body>
        <h2>Hello {name},</h2>
        <p>Congratulations on completing your task on {date}!</p>
        <p>Best regards,<br>Your Team</p>
    </body>
    </html>
    """

    # Send email via SES
    response = ses_client.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [recipient_email],
        },
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body_text},
                'Html': {'Data': body_html}
            }
        }
    )

    print(f"Email sent to {recipient_email}, Message ID: {response['MessageId']}")




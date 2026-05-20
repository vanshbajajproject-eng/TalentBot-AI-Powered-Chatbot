from fastapi import FastAPI, Request
import pymysql

app = FastAPI()

# =========================
# DATABASE CONNECTION FUNCTION
# =========================
def get_db_connection():

    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="project_data",
        port=3306,
        # connect_timeout=5
    )

    return connection


@app.post("/webhook")
async def webhook(request: Request):

    try:

        body = await request.json()

        intent_name = body.get(
            "queryResult", {}
        ).get(
            "intent", {}
        ).get(
            "displayName"
        )

        print("Intent:", intent_name)

        parameters = body.get(
            "queryResult", {}
        ).get(
            "parameters", {}
        )

        # =========================
        # QUERY CONNECT INTENT
        # =========================

        if intent_name == "query-connect":

            company = parameters.get("company-name")
            email = parameters.get("email")
            issue = parameters.get("customer-issues")

            connection = get_db_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO support_requests
            (company_name, email, issue)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (company, email, issue)
            )
            print("Values entered in db")

            connection.commit()

            cursor.close()
            connection.close()

            return {
                "fulfillmentText":
                "Your issue and details have been recorded. A human support representative will contact you after thoroughly looking into it."
            }

            # =========================
            # SOFTWARE DEMO INTENT
            # =========================

        elif intent_name == "software-outsource-connect-info":
            company = parameters.get("company-name")
            email = parameters.get("email")
            size = parameters.get("company-size")

            connection = get_db_connection()

            cursor = connection.cursor()

            query = """
                    INSERT INTO demo_details
                        (company_name, email, company_size)
                    VALUES (%s, %s, %s) \
                    """

            cursor.execute(
                query,
                (company, email, size)
            )
            print("Values entered in db")

            connection.commit()

            cursor.close()
            connection.close()

            return {
                "fulfillmentText":
                    "Thank you! Our team will get back to you within 24 hours."
            }

        # =========================
        # RECRUITMENT INFO INTENT
        # =========================

        elif intent_name == "recruitment-info":

            company = parameters.get("company-name")
            email = parameters.get("email")
            position = parameters.get("job-title")
            candidates = parameters.get("number")
            location = parameters.get("location")
            experience = parameters.get("experience")
            salary = parameters.get("job-package")

            connection = get_db_connection()

            cursor = connection.cursor()

            query = """
            INSERT INTO recruitment_requests
            (
                company_name,
                email,
                job_position,
                candidate_count,
                job_location,
                experience,
                salary_budget
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    company,
                    email,
                    position,
                    candidates,
                    location,
                    experience,
                    salary
                )
            )
            print("Values entered in db")
            connection.commit()

            cursor.close()
            connection.close()

            return {
                "fulfillmentText":
                "Your details are recorded. You will receive the details of suitable candidates at your registered email address."
            }

        return {
            "fulfillmentText":
            "Intent received."
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "fulfillmentText":
            "Something went wrong."
        }
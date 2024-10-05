ATHLETE_TABLE_NAME = "strava_api.athlete"

class StravaAthleteDao:
    def __init__(self, db_service):
        self.db_service = db_service

    def create_athlete(self, athlete_id, athlete_name, refresh_token, email):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO %s (athlete_id, athlete_name, refresh_token, email)
                    VALUES (%s, %s, %s, %s)
                    RETURNING athlete_id
                    """,
                    (ATHLETE_TABLE_NAME, athlete_id, athlete_name, refresh_token, email)
                )
                returned_id = cursor.fetchone()[0]
                connection.commit()
                return returned_id
        except Exception as e:
            connection.rollback()
            print(f"Error creating athlete: {e}")
        finally:
            self.db_service.release_connection(connection)

    def get_athlete(self, athlete_id):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT athlete_id, athlete_name, refresh_token, email
                    FROM %s
                    WHERE athlete_id = %s
                    """,
                    (ATHLETE_TABLE_NAME, athlete_id)
                )
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting athlete: {e}")
        finally:
            self.db_service.release_connection(connection)
    
    def get_athlete_id(self, athlete_name):
        print(f"Getting athlete ID for '{athlete_name}'...")
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT athlete_id
                    FROM %s
                    WHERE athlete_name = %s
                    """,
                    (ATHLETE_TABLE_NAME, athlete_name,)
                )
                result = cursor.fetchone()
                print(f"Result: {result}")
                return result[0]
        except Exception as e:
            print(f"Error getting athlete ID: {e}")
        finally:
            self.db_service.release_connection(connection)

    def update_athlete(self, athlete_id, athlete_name=None, refresh_token=None, email=None):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                query = f"UPDATE ${ATHLETE_TABLE_NAME} SET "
                params = []
                if athlete_name is not None:
                    query += "athlete_name = %s, "
                    params.append(athlete_name)
                if refresh_token is not None:
                    query += "refresh_token = %s, "
                    params.append(refresh_token)
                if email is not None:
                    query += "email = %s, "
                    params.append(email)
                query = query.rstrip(', ') + " WHERE athlete_id = %s"
                params.append(athlete_id)
                cursor.execute(query, tuple(params))
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error updating athlete: {e}")
        finally:
            self.db_service.release_connection(connection)

    def delete_athlete(self, athlete_id):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM %s WHERE athlete_id = %s",
                    (ATHLETE_TABLE_NAME, athlete_id)
                )
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error deleting athlete: {e}")
        finally:
            self.db_service.release_connection(connection)
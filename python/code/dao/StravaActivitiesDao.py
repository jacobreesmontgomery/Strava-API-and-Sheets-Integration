class StravaActivitiesDao:
    def __init__(self, db_service):
        self.db_service = db_service

    def upsert_activity(self, activity_data):
        print(f"Upserting activity to strava_api.activities:\n{activity_data}")
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO strava_api.activities (
                        athlete_id, athlete, activity_id, run, moving_time, distance_mi, pace_min_mi,
                        full_date, time, day, month, date, year, spm_avg, hr_avg, wkt_type,
                        description, total_elev_gain_ft, manual, max_speed_ft_s, calories,
                        achievement_count, kudos_count, comment_count, athlete_count, full_datetime,
                        rpe, rating, avg_power, sleep_rating
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (activity_id) 
                    DO UPDATE SET 
                        athlete_id = EXCLUDED.athlete_id,
                        athlete = EXCLUDED.athlete,
                        run = EXCLUDED.run,
                        moving_time = EXCLUDED.moving_time,
                        distance_mi = EXCLUDED.distance_mi,
                        pace_min_mi = EXCLUDED.pace_min_mi,
                        full_date = EXCLUDED.full_date,
                        time = EXCLUDED.time,
                        day = EXCLUDED.day,
                        month = EXCLUDED.month,
                        date = EXCLUDED.date,
                        year = EXCLUDED.year,
                        spm_avg = EXCLUDED.spm_avg,
                        hr_avg = EXCLUDED.hr_avg,
                        wkt_type = EXCLUDED.wkt_type,
                        description = EXCLUDED.description,
                        total_elev_gain_ft = EXCLUDED.total_elev_gain_ft,
                        manual = EXCLUDED.manual,
                        max_speed_ft_s = EXCLUDED.max_speed_ft_s,
                        calories = EXCLUDED.calories,
                        achievement_count = EXCLUDED.achievement_count,
                        kudos_count = EXCLUDED.kudos_count,
                        comment_count = EXCLUDED.comment_count,
                        athlete_count = EXCLUDED.athlete_count,
                        full_datetime = EXCLUDED.full_datetime,
                        rpe = EXCLUDED.rpe,
                        rating = EXCLUDED.rating,
                        avg_power = EXCLUDED.avg_power,
                        sleep_rating = EXCLUDED.sleep_rating
                    """,
                    activity_data
                )
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error upserting activity: {e}")
        finally:
            self.db_service.release_connection(connection)

    def get_activity(self, activity_id):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM strava_api.activities
                    WHERE activity_id = %s
                    """,
                    (activity_id,)
                )
                return cursor.fetchone()
        except Exception as e:
            print(f"Error getting activity: {e}")
        finally:
            self.db_service.release_connection(connection)

    def update_activity(self, activity_id, **kwargs):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "UPDATE strava_api.activities SET "
                params = []
                for key, value in kwargs.items():
                    query += f"{key} = %s, "
                    params.append(value)
                query = query.rstrip(', ') + " WHERE activity_id = %s"
                params.append(activity_id)
                cursor.execute(query, tuple(params))
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error updating activity: {e}")
        finally:
            self.db_service.release_connection(connection)

    def delete_activity(self, activity_id):
        connection = self.db_service.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM strava_api.activities WHERE activity_id = %s",
                    (activity_id,)
                )
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Error deleting activity: {e}")
        finally:
            self.db_service.release_connection(connection)

import asyncio
import os
import psycopg2
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))
db_url = os.getenv("DATABASE_URL")

async def sync_leaderboards():
    while True:
        print(f"[{datetime.utcnow()}] Running leaderboard sync...")
        try:
            conn = psycopg2.connect(db_url)
            conn.autocommit = True
            cur = conn.cursor()
            
            # 1. Get all active leaderboards
            # For simplicity, assuming if start_time/end_time are null, it's always active
            query_active_leaderboards = """
                SELECT id, linked_gd_currency 
                FROM gd_leaderboard 
                WHERE is_enabled = TRUE 
                AND (gd_leaderboard_start_time IS NULL OR gd_leaderboard_start_time <= NOW())
                AND (gd_leaderboard_end_time IS NULL OR gd_leaderboard_end_time >= NOW())
            """
            cur.execute(query_active_leaderboards)
            active_leaderboards = cur.fetchall()
            
            for lb_id, currency_id in active_leaderboards:
                # 2. Update user scores based on currency balance (assuming ud_user_currency table exists)
                # Since we don't have the exact schema for ud_user_currency yet, this is a placeholder SQL structure
                # In a real scenario, you'd UPSERT from the user's currency balance table.
                
                # Example (Pseudo SQL):
                # INSERT INTO ud_leaderboard_user (linked_ud_user_master, linked_gd_leaderboard, score)
                # SELECT linked_ud_user_master, %s, balance FROM ud_user_currency WHERE linked_gd_currency = %s
                # ON CONFLICT (linked_ud_user_master, linked_gd_leaderboard) DO UPDATE SET score = EXCLUDED.score
                pass
                
                # 3. Recalculate ranks using a window function
                # This assigns a rank based on score descending
                rank_update_query = """
                    WITH RankedUsers AS (
                        SELECT id,
                               RANK() OVER (ORDER BY score DESC) as new_rank
                        FROM ud_leaderboard_user
                        WHERE linked_gd_leaderboard = %s
                    )
                    UPDATE ud_leaderboard_user
                    SET current_rank = RankedUsers.new_rank
                    FROM RankedUsers
                    WHERE ud_leaderboard_user.id = RankedUsers.id;
                """
                cur.execute(rank_update_query, (lb_id,))
                
            cur.close()
            conn.close()
            print(f"[{datetime.utcnow()}] Leaderboard sync complete.")
        except Exception as e:
            print(f"[{datetime.utcnow()}] Error syncing leaderboards: {e}")
            
        # Wait 60 seconds before syncing again
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(sync_leaderboards())

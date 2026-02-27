"""
Neon PostgreSQL Database Integration
Stores job history, results, and metadata
"""
import asyncpg
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.database_url = os.getenv("DATABASE_URL")
    
    async def connect(self):
        """Initialize database connection pool"""
        if not self.database_url:
            print("⚠️ DATABASE_URL not set, database features disabled")
            return
        
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            await self.init_tables()
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            self.pool = None
    
    async def disconnect(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()
            print("🔌 Database disconnected")
    
    async def init_tables(self):
        """Create tables if they don't exist"""
        if not self.pool:
            return
        
        async with self.pool.acquire() as conn:
            # Jobs table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    format TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    completed_at TIMESTAMPTZ,
                    file_extension TEXT,
                    content_type TEXT,
                    proxy_server TEXT,
                    headless BOOLEAN DEFAULT FALSE,
                    streaming_enabled BOOLEAN DEFAULT FALSE,
                    error_message TEXT
                )
            """)
            
            # Job results table (stores extracted content metadata)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS job_results (
                    id SERIAL PRIMARY KEY,
                    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
                    content_length INTEGER,
                    extraction_time TIMESTAMPTZ DEFAULT NOW(),
                    format TEXT,
                    metadata JSONB
                )
            """)
            
            # Proxy usage tracking
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS proxy_stats (
                    id SERIAL PRIMARY KEY,
                    job_id TEXT REFERENCES jobs(id) ON DELETE SET NULL,
                    proxy_server TEXT,
                    success BOOLEAN,
                    error_message TEXT,
                    recorded_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            print("📊 Database tables initialized")
    
    async def create_job(self, job_id: str, prompt: str, format: str, 
                        headless: bool = False, streaming_enabled: bool = False,
                        proxy_server: Optional[str] = None) -> bool:
        """Create a new job record"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO jobs (id, prompt, format, headless, streaming_enabled, proxy_server, status)
                    VALUES ($1, $2, $3, $4, $5, $6, 'running')
                """, job_id, prompt, format, headless, streaming_enabled, proxy_server)
            return True
        except Exception as e:
            print(f"❌ Failed to create job: {e}")
            return False
    
    async def update_job_status(self, job_id: str, status: str, 
                               error_message: Optional[str] = None) -> bool:
        """Update job status"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                completed_at = datetime.utcnow() if status in ['completed', 'failed'] else None
                await conn.execute("""
                    UPDATE jobs 
                    SET status = $2, 
                        completed_at = $3,
                        error_message = $4
                    WHERE id = $1
                """, job_id, status, completed_at, error_message)
            return True
        except Exception as e:
            print(f"❌ Failed to update job status: {e}")
            return False
    
    async def update_job_info(self, job_id: str, file_extension: str, 
                             content_type: str) -> bool:
        """Update job file information"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    UPDATE jobs 
                    SET file_extension = $2, content_type = $3
                    WHERE id = $1
                """, job_id, file_extension, content_type)
            return True
        except Exception as e:
            print(f"❌ Failed to update job info: {e}")
            return False
    
    async def save_job_result(self, job_id: str, content_length: int,
                             format: str, metadata: Dict[str, Any]) -> bool:
        """Save job result metadata"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO job_results (job_id, content_length, format, metadata)
                    VALUES ($1, $2, $3, $4)
                """, job_id, content_length, format, json.dumps(metadata))
            return True
        except Exception as e:
            print(f"❌ Failed to save job result: {e}")
            return False
    
    async def log_proxy_usage(self, job_id: str, proxy_server: str,
                             success: bool, error_message: Optional[str] = None) -> bool:
        """Log proxy usage for a job"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO proxy_stats (job_id, proxy_server, success, error_message)
                    VALUES ($1, $2, $3, $4)
                """, job_id, proxy_server, success, error_message)
            return True
        except Exception as e:
            print(f"❌ Failed to log proxy usage: {e}")
            return False
    
    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        if not self.pool:
            return None
        
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM jobs WHERE id = $1
                """, job_id)
                
                if row:
                    return dict(row)
                return None
        except Exception as e:
            print(f"❌ Failed to get job: {e}")
            return None
    
    async def get_all_jobs(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all jobs with pagination"""
        if not self.pool:
            return []
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT * FROM jobs 
                    ORDER BY created_at DESC 
                    LIMIT $1 OFFSET $2
                """, limit, offset)
                
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Failed to get jobs: {e}")
            return []
    
    async def get_job_stats(self) -> Dict[str, Any]:
        """Get overall job statistics"""
        if not self.pool:
            return {}
        
        try:
            async with self.pool.acquire() as conn:
                stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_jobs,
                        COUNT(*) FILTER (WHERE status = 'completed') as completed,
                        COUNT(*) FILTER (WHERE status = 'failed') as failed,
                        COUNT(*) FILTER (WHERE status = 'running') as running
                    FROM jobs
                """)
                return dict(stats) if stats else {}
        except Exception as e:
            print(f"❌ Failed to get stats: {e}")
            return {}
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job and its results"""
        if not self.pool:
            return False
        
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM jobs WHERE id = $1", job_id)
            return True
        except Exception as e:
            print(f"❌ Failed to delete job: {e}")
            return False

# Global database instance
db = Database()

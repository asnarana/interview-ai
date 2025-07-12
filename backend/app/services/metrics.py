import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

#key features are performance tracking ( so eye contact, sentiment, etc)
# keeps last 100 perforamance entries to prevent file from growing too large
# counts diff types of failures tracks statistics by date , and removes older data.
#this data will be written back to metric json file. The api endpoint will call this service to get the metrics.

class MetricsService:
    def __init__(self, metrics_dir: str = "metrics"):
        # initialize metrics directory and file paths
        self.metrics_dir = metrics_dir
        os.makedirs(metrics_dir, exist_ok=True)
        self.metrics_file = os.path.join(metrics_dir, "app_metrics.json")
        self.load_metrics()
    
    def load_metrics(self):
        try:
            if os.path.exists(self.metrics_file):
                # load existing metrics from json file
                with open(self.metrics_file, 'r') as f:
                    self.metrics = json.load(f)
            else:
                # initialize new metrics structure if file doesn't exist
                self.metrics = self._initialize_metrics()
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            self.metrics = self._initialize_metrics()
    
    def _initialize_metrics(self) -> Dict:
        return {
            "startup_time": datetime.now().isoformat(),
            "total_interviews": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "average_processing_time": 0.0,
            "total_processing_time": 0.0,
            "daily_stats": {},
            "error_counts": {},
            "performance_metrics": {
                "eye_contact_scores": [],
                "sentiment_scores": [],
                "speech_rates": [],
                "overall_scores": []
            }
        }
    
    def save_metrics(self):
        try:
            # write metrics to json file with proper formatting
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def record_interview_created(self, interview_id: int, title: str):
        # increment total interview count
        self.metrics["total_interviews"] += 1
        # update daily statistics
        self._update_daily_stats("interviews_created", 1)
        logger.info(f"📊 Metrics: Interview created - ID: {interview_id}, Title: {title}")
        self.save_metrics()
    
    def record_analysis_success(self, interview_id: int, processing_time: float, 
                               eye_contact: float, sentiment_score: float, 
                               speech_rate: float, overall_score: float):
        # increment successful analysis count
        self.metrics["successful_analyses"] += 1
        # update total and average processing time
        self.metrics["total_processing_time"] += processing_time
        self.metrics["average_processing_time"] = (
            self.metrics["total_processing_time"] / self.metrics["successful_analyses"]
        )
        
        # record performance metrics for analysis
        self.metrics["performance_metrics"]["eye_contact_scores"].append(eye_contact)
        self.metrics["performance_metrics"]["sentiment_scores"].append(sentiment_score)
        self.metrics["performance_metrics"]["speech_rates"].append(speech_rate)
        self.metrics["performance_metrics"]["overall_scores"].append(overall_score)
        
        # keep only last 100 entries to prevent file from growing too large
        for key in self.metrics["performance_metrics"]:
            if len(self.metrics["performance_metrics"][key]) > 100:
                self.metrics["performance_metrics"][key] = self.metrics["performance_metrics"][key][-100:]
        
        # update daily statistics
        self._update_daily_stats("analyses_completed", 1)
        self._update_daily_stats("total_processing_time", processing_time)
        
        logger.info(f"📊 Metrics: Analysis success - ID: {interview_id}, Time: {processing_time:.2f}s, Score: {overall_score}%")
        self.save_metrics()
    
    def record_analysis_failure(self, error_type: str, processing_time: float):
        # increment failed analysis count
        self.metrics["failed_analyses"] += 1
        # track error counts by type
        if error_type not in self.metrics["error_counts"]:
            self.metrics["error_counts"][error_type] = 0
        self.metrics["error_counts"][error_type] += 1
        
        # update daily statistics
        self._update_daily_stats("analyses_failed", 1)
        
        logger.warning(f"📊 Metrics: Analysis failed - Error: {error_type}, Time: {processing_time:.2f}s")
        self.save_metrics()
    
    def record_api_request(self, endpoint: str, method: str, status_code: int, processing_time: float):
        today = datetime.now().strftime("%Y-%m-%d")
        # initialize daily stats if not exists
        if today not in self.metrics["daily_stats"]:
            self.metrics["daily_stats"][today] = {
                "interviews_created": 0,
                "analyses_completed": 0,
                "analyses_failed": 0,
                "total_processing_time": 0.0,
                "api_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0
            }
        
        # increment api request counters
        self.metrics["daily_stats"][today]["api_requests"] += 1
        if 200 <= status_code < 400:
            self.metrics["daily_stats"][today]["successful_requests"] += 1
        else:
            self.metrics["daily_stats"][today]["failed_requests"] += 1
    
    def _update_daily_stats(self, stat_name: str, value: float):
        today = datetime.now().strftime("%Y-%m-%d")
        # initialize daily stats structure if not exists
        if today not in self.metrics["daily_stats"]:
            self.metrics["daily_stats"][today] = {
                "interviews_created": 0,
                "analyses_completed": 0,
                "analyses_failed": 0,
                "total_processing_time": 0.0,
                "api_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0
            }
        
        # update specific statistic
        if stat_name in self.metrics["daily_stats"][today]:
            self.metrics["daily_stats"][today][stat_name] += value
        else:
            self.metrics["daily_stats"][today][stat_name] = value
    
    def get_summary(self) -> Dict:
        return {
            "total_interviews": self.metrics["total_interviews"],
            "successful_analyses": self.metrics["successful_analyses"],
            "failed_analyses": self.metrics["failed_analyses"],
            "success_rate": (
                self.metrics["successful_analyses"] / 
                max(self.metrics["successful_analyses"] + self.metrics["failed_analyses"], 1) * 100
            ),
            "average_processing_time": self.metrics["average_processing_time"],
            "uptime": self._calculate_uptime(),
            "recent_errors": dict(list(self.metrics["error_counts"].items())[-5:]),  # last 5 errors
            "today_stats": self._get_today_stats()
        }
    
    def _calculate_uptime(self) -> str:
        try:
            # parse startup time and calculate difference
            startup_time = datetime.fromisoformat(self.metrics["startup_time"])
            uptime = datetime.now() - startup_time
            return str(uptime).split('.')[0]  # remove microseconds
        except:
            return "Unknown"
    # getting the metrics for today
    def _get_today_stats(self) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.metrics["daily_stats"].get(today, {
            "interviews_created": 0,
            "analyses_completed": 0,
            "analyses_failed": 0,
            "api_requests": 0
        })
    #keeps only last 30 days of data
    def cleanup_old_data(self, days_to_keep: int = 30):
        # calculate cutoff date for data retention
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        dates_to_remove = []
        # identify dates to remove
        for date_str in self.metrics["daily_stats"]:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj < cutoff_date:
                    dates_to_remove.append(date_str)
            except:
                continue
        
        # remove old data
        for date_str in dates_to_remove:
            del self.metrics["daily_stats"][date_str]
        
        if dates_to_remove:
            logger.info(f" Cleaned up {len(dates_to_remove)} old daily statistics")
            self.save_metrics()

# global metrics service instance
metrics_service = MetricsService() 
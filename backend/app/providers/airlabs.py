"""
AirLabs API 프로바이더 모듈
일본 국내선 항공편 검색 (Peach Aviation 등)
"""
import httpx
import asyncio
from typing import List, Optional, Dict, Any
from datetime import date
import logging
import time
from app.config import settings
from app.models.flight_segment import FlightSegment
from app.utils.date_utils import DateUtils

logger = logging.getLogger(__name__)

# HTTP 클라이언트 설정
HTTP_TIMEOUT = 10.0  # 10초 타임아웃
MAX_RETRIES = 3  # 최대 재시도 횟수
RETRY_DELAY_BASE = 1.0  # 재시도 지연 시간 (초)


class AirLabsProvider:
    """AirLabs API 프로바이더 (Peach Aviation 검색)"""
    
    def __init__(self):
        self.api_key = settings.airlabs_api_key
        self.base_url = settings.airlabs_base_url
        # HTTP 클라이언트 (재사용)
        self.client = httpx.AsyncClient(
            timeout=HTTP_TIMEOUT,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
    
    async def search_peach_flight(
        self,
        origin: str,
        destination: str,
        departure_date: date
    ) -> Optional[FlightSegment]:
        """
        Peach Aviation 항공편 검색 (재시도 포함)
        
        Args:
            origin: 출발 공항 코드
            destination: 도착 공항 코드
            departure_date: 출발 날짜
        
        Returns:
            최저가 FlightSegment 또는 None
        """
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"AirLabs (Peach) 검색: {origin} → {destination} ({departure_date})")
                
                # AirLabs API 호출
                date_str = DateUtils.format_date_for_api(departure_date)
                api_url = f"{self.base_url}/flights"
                
                params = {
                    "api_key": self.api_key,
                    "dep_iata": origin,
                    "arr_iata": destination,
                    "date": date_str
                }
                
                response = await self.client.get(api_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # API 응답을 FlightSegment로 변환
                segments = self.normalize_response(data)
                if segments:
                    return segments[0]  # 최저가 반환
                return None
                
            except httpx.HTTPStatusError as e:
                logger.error(f"❌ AirLabs API 호출 실패 (HTTP {e.response.status_code}): {e.response.text}")
                if attempt == MAX_RETRIES - 1:
                    return None
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"AirLabs 검색 실패 (최대 재시도 초과): {e}")
                    return None
                delay = RETRY_DELAY_BASE * (2 ** attempt)  # Exponential backoff
                logger.warning(f"AirLabs 검색 실패 (재시도 {attempt + 1}/{MAX_RETRIES}): {e}, {delay}초 후 재시도")
                await asyncio.sleep(delay)
        
        return None
    
    async def search_multiple_routes(
        self,
        routes: List[tuple[str, str, date]]
    ) -> List[Optional[FlightSegment]]:
        """여러 경로 동시 검색"""
        tasks = [
            self.search_peach_flight(origin, dest, dep_date)
            for origin, dest, dep_date in routes
        ]
        results = await asyncio.gather(*tasks)
        return results
    
    def normalize_response(self, api_response: Dict[str, Any]) -> List[FlightSegment]:
        """
        AirLabs API 응답을 표준 FlightSegment 형식으로 변환
        
        실제 구현 시 API 응답 구조에 맞게 파싱
        """
        # 실제 구현 필요
        segments = []
        # 예시 파싱 로직 (실제 API 응답 구조에 맞게 수정 필요)
        return segments
    
    async def close(self):
        """리소스 정리 (HTTP 클라이언트 종료)"""
        await self.client.aclose()


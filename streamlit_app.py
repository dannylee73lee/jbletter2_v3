import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta
import base64
import os
import re
import requests
import json
import traceback
import markdown

# 기본 콘텐츠 제공 함수들
def get_default_tips_content():
    """기본 AT/DT 팁 콘텐츠 반환"""
    return """
    <div class="tip-title">이번 주 팁: 효과적인 프롬프트 작성의 기본 원칙</div>
   
    <p>AI를 더 효과적으로 활용하기 위해서는 명확하고 구체적인 프롬프트를 작성하는 것이 중요합니다. Chain of Thought와 Chain of Draft 기법을 활용하면 더 정확한 결과를 얻을 수 있습니다.</p>
   
    <div class="prompt-examples-title">핵심 프롬프트 예시:</div>
   
    <div class="prompt-template">
    <div class="template-title">- 첫 번째 프롬프트 템플릿 (Chain of Thought 활용):</div>
    <div class="template-content">
    <div class="example-label">예시:</div>
    <div class="example-content">이 보고서를 요약해주세요.</div>
    <div class="prompt-label">프롬프트:</div>
    <div class="prompt-content">이 보고서의 핵심 주제와 중요한 발견 사항을 파악하고, 주요 결론을 도출해주세요. 단계별로 생각하며 요약해주세요.</div>
    </div>
    </div>
   
    <div class="prompt-template">
    <div class="template-title">- 두 번째 프롬프트 템플릿 (Chain of Draft 활용):</div>
    <div class="template-content">
    <div class="example-label">예시:</div>
    <div class="example-content">이메일을 작성해주세요.</div>
    <div class="prompt-label">프롬프트:</div>
    <div class="prompt-content">고객에게 보낼 이메일을 작성해주세요. 먼저 초안을 작성하고, 그 다음 더 공손하고 전문적인 어조로 다듬어주세요.</div>
    </div>
    </div>
   
    <div class="prompt-template">
    <div class="template-title">- 세 번째 프롬프트 템플릿 (Chain of Thought와 Chain of Draft 결합):</div>
    <div class="template-content">
    <div class="example-label">예시:</div>
    <div class="example-content">신제품 출시 보도자료를 작성해주세요.</div>
    <div class="prompt-label">프롬프트:</div>
    <div class="prompt-content">신제품 출시 보도자료를 작성하기 위해, 먼저 포함해야 할 핵심 내용을 파악하고, 이를 바탕으로 초안을 작성한 후, 전문적이고 간결한 최종본으로 발전시켜주세요.</div>
    </div>
    </div>
   
    <div class="tip-footer">다음 주에는 특정 업무별 최적의 프롬프트 템플릿에 대해 알려드리겠습니다.</div>
    """

def get_default_success_story():
    """기본 성공 사례 콘텐츠 반환"""
    return """
    <h2>삼성전자의 AI 혁신 사례</h2>
   
    <p>삼성전자는 생산 라인의 불량품 검출률을 높이기 위해 AI 비전 시스템 도입을 결정했습니다. 기존의 수동 검사 방식으로는 약 92%의 정확도를 보였으며, 검사 시간이 길어 생산성 저하의 원인이 되었습니다. 특히 미세한 결함을 감지하는 데 어려움이 있었습니다.</p>
   
    <p>삼성전자는 딥러닝 기반의 컴퓨터 비전 시스템을 구축하고, 수십만 장의 정상 및 불량 제품 이미지로 AI 모델을 학습시켰습니다. 이 시스템은 실시간으로 제품을 스캔하고 결함을 자동으로 식별하며, 결함의 유형과 심각성까지 분류할 수 있도록 설계되었습니다.</p>
   
    <p>AI 시스템 도입 후 불량품 검출 정확도가 92%에서 98.5%로 향상되었으며, 검사 시간은 60% 단축되었습니다. 이로 인해 연간 약 150억 원의 비용 절감 효과를 얻었으며, 제품 품질 향상으로 고객 반품률도 15% 감소했습니다.</p>
   
    <h2>Google의 AI 혁신 사례</h2>
   
    <p>Google은 데이터 센터의 에너지 효율성을 개선하기 위해 DeepMind AI 시스템을 도입했습니다. 데이터 센터는 전 세계 전력 소비의 상당 부분을 차지하며, 냉각 시스템이 특히 많은 에너지를 소비합니다. 기존의 냉각 시스템은 수동 설정과 기본 알고리즘에 의존하여 최적화가 어려웠습니다.</p>
   
    <p>Google은 DeepMind의 강화학습 AI 시스템을 활용하여 수천 개의 센서 데이터를 분석하고 냉각 시스템을 자동으로 최적화하는 솔루션을 개발했습니다. 이 AI는 외부 온도, 서버 부하, 전력 사용량 등 다양한 변수를 고려하여 실시간으로 냉각 시스템을 조정합니다.</p>
   
    <p>AI 시스템 도입 결과, Google 데이터 센터의 냉각 에너지 소비가 약 40% 감소했으며, 전체 PUE(전력 사용 효율성)가 15% 개선되었습니다. 이는 연간 수백만 달러의 비용 절감과 탄소 배출량 감소로 이어졌으며, 다른 데이터 센터에도 적용 가능한 모델을 제시했습니다.</p>
    """

def get_default_ai_use_case():
    """기본 AI 활용사례 콘텐츠 반환"""
    return """
    <h2>AI를 활용한 문서 요약 및 번역 사례</h2>
   
    <p><strong>요약:</strong> 다국적 기업에서 여러 언어로 된 보고서와 문서를 효율적으로 처리하기 위해 AI 요약 및 번역 시스템을 도입했습니다. 이를 통해 문서 처리 시간을 80% 단축하고 국가 간 정보 공유를 원활하게 개선했습니다.</p>
   
    <p><strong>단계별 방법:</strong></p>
    <ol>
      <li>GPT 기반 문서 요약 시스템 구축으로 긴 문서의 핵심 내용 추출</li>
      <li>다국어 번역 모델을 통합하여 10개 이상 언어 간 번역 지원</li>
      <li>전문 용어 사전을 구축하여 산업 특화 번역 정확도 향상</li>
      <li>문서 형식을 유지하며 요약 및 번역 결과를 원본과 함께 제공</li>
    </ol>
   
    <p><strong>추천 프롬프트:</strong> "다음 기술 보고서를 3가지 핵심 포인트로 요약하고, 각 포인트에 대한 간략한 설명을 추가해주세요. 그 후 요약된 내용을 [대상 언어]로 번역해주세요. 산업 용어는 정확하게 번역하고, 번역된 용어 옆에 영어 원문을 괄호 안에 표기해주세요."</p>
   
    <p style="text-align: right; margin-top: 15px;"><a href="https://www.deepl.com" target="_blank" style="color: #ff5722; text-decoration: none; font-weight: bold;">사례 확인해보기 →</a></p>
    <p style="font-size: 8pt; text-align: right; color: #666;">출처: DeepL 사례연구</p>
    """

def get_highlight_suggestions():
    """다양한 하이라이트 메시지 제안"""
    suggestions = [
        {
            "title": "시선이 바뀌면 세상이 달라집니다",
            "subtitle": "어제까지 당연하다고 생각했던 것들이 오늘은 왜 이렇게 이상해 보일까요? 🤔",
            "description": "답은 간단합니다.\n시선이 바뀌었기 때문입니다. 🔍"
        },
        {
            "title": "AI와 함께하는 새로운 시작",
            "subtitle": "복잡해 보이는 기술도 하나씩 알아가면 친숙해집니다 ✨",
            "description": "오늘부터 함께 배워볼까요? 🚀"
        },
        {
            "title": "작은 변화가 큰 혁신을 만듭니다",
            "subtitle": "거창한 계획보다 작은 실행이 더 중요해요 💪",
            "description": "지금 바로 시작해보세요! 🎯"
        }
    ]
    return suggestions

def convert_markdown_to_html(text):
    """마크다운 텍스트를 HTML로 변환합니다."""
    # AT/DT 팁 섹션 특별 처리를 위한 전처리
    if "이번 주 팁:" in text or "핵심 프롬프트 예시" in text:
        # 기존 특별 처리 유지하되 정규식 패턴 단순화
        text = re.sub(r'^## 이번 주 팁: (.*?)$', r'<div class="tip-title">이번 주 팁: \1</div>', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*핵심 프롬프트 예시:\*\*', r'<div class="prompt-examples-title">핵심 프롬프트 예시:</div>', text)
       
        # 프롬프트 템플릿 처리 - 더 효율적인 패턴 사용
        template_patterns = [
            (r'- (첫 번째 프롬프트 템플릿 \(Chain of Thought 활용\):)(.*?)(?=- 두 번째 프롬프트|\$)', 1, 2),
            (r'- (두 번째 프롬프트 템플릿 \(Chain of Draft 활용\):)(.*?)(?=- 세 번째 프롬프트|\$)', 1, 2),
            (r'- (세 번째 프롬프트 템플릿 \(Chain of Thought와 Chain of Draft 결합\):)(.*?)(?=이 팁을|\$)', 1, 2)
        ]
       
        for pattern, title_group, content_group in template_patterns:
            text = re.sub(
                pattern,
                lambda m: f'<div class="prompt-template">'
                          f'<div class="template-title">{m.group(title_group)}</div>'
                          f'<div class="template-content">{m.group(content_group)}</div>'
                          f'</div>',
                text,
                flags=re.DOTALL
            )
       
        # 예시와 프롬프트 처리 - 한 번의 정규식으로 처리
        text = re.sub(
            r'<div class="template-content">(.*?)예시:(.*?)프롬프트:(.*?)</div>',
            r'<div class="template-content">'
            r'<div class="example-label">예시:</div>'
            r'<div class="example-content">\2</div>'
            r'<div class="prompt-label">프롬프트:</div>'
            r'<div class="prompt-content">\3</div>'
            r'</div>',
            text,
            flags=re.DOTALL
        )
       
        # 마지막 문장 스타일 적용
        if "다음 주에는" in text:
            text = re.sub(r'(다음 주에는.*?\.)', r'<div class="tip-footer">\1</div>', text)
   
    # markdown 라이브러리로 기본 변환 처리
    html = markdown.markdown(text)
   
    # 추가 후처리 - 특별한 강조 태그 등
    html = re.sub(r'\[강조\](.*?)\[\/강조\]', r'<span style="color:#e74c3c; font-weight:bold;">\1</span>', html)
   
    return html

def fetch_news(api_type, query, days=7, language="en", display=5, **kwargs):
    """통합된 뉴스 수집 함수. API 유형에 따라 다른 방식으로 데이터 수집"""
   
    # 날짜 범위 계산
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
   
    try:
        if api_type == 'newsapi':
            api_key = kwargs.get('api_key')
            if not api_key:
                raise ValueError("NewsAPI 키가 필요합니다")
               
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': language,
                'apiKey': api_key
            }
           
            response = requests.get(url, params=params)
            if response.status_code == 200:
                news_data = response.json()
                return news_data['articles'][:display]  # display 개수만큼 반환
            else:
                raise Exception(f"API 응답 오류: {response.status_code} - {response.text}")
               
        elif api_type == 'naver':
            client_id = kwargs.get('client_id')
            client_secret = kwargs.get('client_secret')
           
            if not client_id or not client_secret:
                raise ValueError("네이버 API 인증 정보가 필요합니다")
               
            url = "https://openapi.naver.com/v1/search/news.json"
            headers = {
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret
            }
            params = {
                "query": query,
                "display": 100,  # 많이 가져와서 필터링
                "sort": "date"
            }
           
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                result = response.json()
               
                # 최근 days일 내의 뉴스만 필터링
                filtered_items = []
                cutoff_date = start_date
               
                for item in result['items']:
                    try:
                        pub_date_str = item.get('pubDate')
                        if pub_date_str:
                            pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
                            pub_date = pub_date.replace(tzinfo=None)
                           
                            if pub_date >= cutoff_date:
                                # HTML 태그 제거
                                item['title'] = item['title'].replace("<b>", "").replace("</b>", "")
                                item['description'] = item['description'].replace("<b>", "").replace("</b>", "")
                                filtered_items.append(item)
                    except Exception as e:
                        print(f"날짜 파싱 오류 (포함됨): {str(e)}")
                        filtered_items.append(item)
               
                return filtered_items[:display]  # display 개수만큼 반환
            else:
                raise Exception(f"API 응답 오류: {response.status_code} - {response.text}")
               
        elif api_type == 'naver_search':
            client_id = kwargs.get('client_id')
            client_secret = kwargs.get('client_secret')
           
            if not client_id or not client_secret:
                raise ValueError("네이버 API 인증 정보가 필요합니다")
               
            url = "https://openapi.naver.com/v1/search/web.json"  # 웹 문서 검색 API로 변경
            headers = {
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret
            }
           
            # 여러 소스에서 검색을 위한 서브쿼리 구성
            sub_queries = kwargs.get('sub_queries', [f"{query} 사례", f"{query} 기업", f"{query} 활용"])
           
            all_items = []
            for search_query in sub_queries:
                try:
                    params = {
                        "query": search_query,
                        "display": display,
                        "sort": "date"
                    }
                   
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        result = response.json()
                        all_items.extend(result['items'])
                    else:
                        print(f"서브쿼리 '{search_query}' 검색 실패: {response.status_code}")
                except Exception as e:
                    print(f"서브쿼리 '{search_query}' 처리 오류: {str(e)}")
           
            # 중복 제거 및 HTML 태그 제거
            unique_items = []
            unique_titles = set()
           
            for item in all_items:
                clean_title = item['title'].replace("<b>", "").replace("</b>", "")
                if clean_title not in unique_titles:
                    # HTML 태그 제거
                    item['title'] = clean_title
                    item['description'] = item['description'].replace("<b>", "").replace("</b>", "")
                    unique_titles.add(clean_title)
                    unique_items.append(item)
           
            return unique_items[:display]
   
    except Exception as e:
        print(f"{api_type} 데이터 수집 오류: {str(e)}")
        return []  # 오류 발생시 빈 리스트 반환

def create_naver_news_section(news_items, section_title):
    """네이버 뉴스 섹션 HTML 생성 함수"""
    content = f"<h2>{section_title}</h2>"
   
    if not news_items:
        content += "<p>최근 7일 이내의 관련 뉴스가 없습니다.</p>"
    else:
        for i, article in enumerate(news_items):
            # 날짜 표시 추가
            pub_date_str = article.get('pubDate', '')
            pub_date_display = ""
            try:
                if pub_date_str:
                    pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
                    pub_date_display = pub_date.strftime('%Y년 %m월 %d일')
            except Exception:
                pub_date_display = "날짜 정보 없음"
           
            content += f"<h3>{article['title']}</h3>"
            content += f"<p><small>게시일: {pub_date_display}</small></p>"
            content += f"<p>{article['description']}</p>"
            content += f"<p><a href='{article['link']}' target='_blank'>원문 보기</a> | 출처: {article.get('originallink', article['link'])}</p>"
           
            if i < len(news_items) - 1:  # 마지막 뉴스가 아닌 경우 구분선 추가
                content += "<hr>"
   
    return content

def generate_ai_content(openai_api_key, content_type, custom_prompt=None, **kwargs):
    """통합된 OpenAI 콘텐츠 생성 함수"""
   
    if not openai_api_key:
        # API 키가 없는 경우 기본 콘텐츠 반환
        default_contents = {
            'main_news': "<p>API 키가 제공되지 않아 콘텐츠를 생성할 수 없습니다.</p>",
            'aidt_tips': get_default_tips_content(),
            'success_story': get_default_success_story(),
            'ai_use_case': get_default_ai_use_case()
        }
        return default_contents.get(content_type, "<p>API 키가 제공되지 않아 콘텐츠를 생성할 수 없습니다.</p>")
   
    # 프롬프트 템플릿 정의
    prompt_templates = {
        'main_news': """
        AIDT Weekly 뉴스레터의 '주요 소식' 섹션을 생성해주세요.
        오늘 날짜는 {date}입니다. 아래는 두 종류의 뉴스 기사입니다:
       
        === OpenAI 관련 뉴스 ===
        {openai_news_info}
       
        === 일반 뉴스 ===
        {news_info}
       
        총 2개의 주요 소식을 다음 형식으로 작성해주세요:
       
        1. 먼저 OpenAI 관련 뉴스에서 가장 중요하고 관련성 높은 1개의 소식을 선택하여 작성하세요.
        2. 그 다음 일반 뉴스에서 가장 중요하고 관련성 높은 1개의 소식을 선택하여 작성하세요.
       
        각 소식은 다음 형식으로 작성해주세요:
        ## [주제]의 [핵심 강점/특징]은 [주목할만합니다/확인됐습니다/중요합니다].
       
        간략한 내용을 1-2문장으로 작성하세요. 내용은 특정 기술이나 서비스, 기업의 최신 소식을 다루고,
        핵심 내용만 포함해주세요. 그리고 왜 중요한지를 강조해주세요.
       
        구체적인 수치나 인용구가 있다면 추가해주세요.
       
        각 소식의 마지막에는 뉴스 기사의 발행일과 출처를 반드시 "[출처 제목](출처 URL)" 형식으로 포함하세요.
       
        모든 주제는 반드시 제공된 실제 뉴스 기사에서만 추출해야 합니다. 가상의 정보나 사실이 아닌 내용은 절대 포함하지 마세요.
        각 소식 사이에 충분한 공백을 두어 가독성을 높여주세요.
        """,
       
        'aidt_tips': """
        AIDT Weekly 뉴스레터의 '이번 주 AT/DT 팁' 섹션을 생성해주세요.
       
        이번 주 팁 주제는 "{current_topic}"입니다.
       
        이 주제에 대해 다음 형식으로 실용적인 팁을 작성해주세요:
       
        ## 이번 주 팁: [주제에 맞는 구체적인 팁 제목]
       
        팁에 대한 배경과 중요성을 2-3문장으로 간결하게 설명해주세요. AI 기본기와 관련된 내용을 포함하세요.
        특히, 영어 용어는 한글로 번역하지 말고 그대로 사용해주세요 (예: "Chain of Thought", "Chain of Draft").
       
        **핵심 프롬프트 예시:**
        - 첫 번째 프롬프트 템플릿 (Chain of Thought 활용):
          예시: [이 문제/작업에 대한 실제 예시를 제시하세요]
          프롬프트: [구체적인 Chain of Thought 프롬프트 템플릿을 작성하세요]
       
        - 두 번째 프롬프트 템플릿 (Chain of Draft 활용):
          예시: [이 문제/작업에 대한 실제 예시를 제시하세요]
          프롬프트: [구체적인 Chain of Draft 프롬프트 템플릿을 작성하세요]
       
        - 세 번째 프롬프트 템플릿 (Chain of Thought와 Chain of Draft 결합):
          예시: [이 문제/작업에 대한 실제 예시를 제시하세요]
          프롬프트: [두 기법을 결합한 프롬프트 템플릿을 작성하세요]
       
        이 팁을 활용했을 때의 업무 효율성 향상이나 결과물 품질 개선 등 구체적인 이점을 한 문장으로 작성해주세요.
       
        다음 주에는 다른 AI 기본기 팁을 알려드리겠습니다.
        """,
       
        'success_story': """
        AIDT Weekly 뉴스레터의 '성공 사례' 섹션을 생성해주세요.
        한국 기업 사례 1개와 외국 기업 사례 1개를 생성해야 합니다.
        각 사례는 제목과 3개의 단락으로 구성되어야 합니다.
        각 단락은 3~4줄로 구성하고, 구체적인 내용과 핵심 정보를 포함해야 합니다.
        단락 사이에는 한 줄을 띄워서 가독성을 높여주세요.
       
        형식:
       
        ## [한국 기업명]의 AI 혁신 사례
       
        첫 번째 단락에서는 기업이 직면한 문제와 배경을 상세히 설명합니다. 구체적인 수치나 상황을 포함하여 3~4줄로 작성해주세요. 이 부분에서는 독자가 왜 이 기업이 AI 솔루션을 필요로 했는지 이해할 수 있도록 해주세요.
       
        두 번째 단락에서는 기업이 도입한 AI 솔루션을 상세히 설명합니다. 어떤 기술을 사용했는지, 어떻게 구현했는지, 특별한 접근 방식은 무엇이었는지 등을 포함하여 3~4줄로 작성해주세요.
       
        세 번째 단락에서는 AI 도입 후 얻은 구체적인 성과와 결과를 설명합니다. 가능한 한 정량적인 수치(비용 절감, 효율성 증가, 고객 만족도 향상 등)를 포함하여 3~4줄로 작성해주세요.
       
        ## [외국 기업명]의 AI 혁신 사례
       
        첫 번째 단락에서는 기업이 직면한 문제와 배경을 상세히 설명합니다. 구체적인 수치나 상황을 포함하여 3~4줄로 작성해주세요. 이 부분에서는 독자가 왜 이 기업이 AI 솔루션을 필요로 했는지 이해할 수 있도록 해주세요.
       
        두 번째 단락에서는 기업이 도입한 AI 솔루션을 상세히 설명합니다. 어떤 기술을 사용했는지, 어떻게 구현했는지, 특별한 접근 방식은 무엇이었는지 등을 포함하여 3~4줄로 작성해주세요.
       
        세 번째 단락에서는 AI 도입 후 얻은 구체적인 성과와 결과를 설명합니다. 가능한 한 정량적인 수치(비용 절감, 효율성 증가, 고객 만족도 향상 등)를 포함하여 3~4줄로 작성해주세요.
        """,
       
        'ai_use_case': """
        AIDT Weekly 뉴스레터의 'AI 활용사례' 섹션을 생성해주세요.
        아래는 검색된 실제 AI 활용사례 정보입니다:
       
        {use_case_info}
       
        위 검색 결과 중에서 가장 유용하고 구체적인 활용사례를 선택하여 다음 형식으로 내용을 작성해주세요:
       
        ## [활용사례 제목] - 제목은 1줄로 명확하게
       
        **요약:** 배경과 중요성을 2-3문장으로 간결하게 설명해주세요.
       
        **단계별 방법:** AI 솔루션을 상세히 설명합니다. 어떤 기술을 사용했는지, 어떻게 구현했는지, 특별한 접근 방식은 무엇이었는지 등을 포함하여 3~4줄로 작성해주세요.
       
        **추천 프롬프트:** 이 활용사례를 더 효과적으로 활용하기 위한 구체적이고 명확한 프롬프트 예시를 작성해주세요.
       
        모든 내용은 반드시 제공된 검색 결과에서만 추출해야 합니다. 가상의 정보나 사실이 아닌 내용은 절대 포함하지 마세요.
        내용은 마크다운 형식으로 작성해주세요.
        """
    }
   
    # 사용자 정의 프롬프트 사용 또는 기본 템플릿 채우기
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = prompt_templates.get(content_type, "").format(**kwargs)
   
    try:
        # OpenAI 클라이언트 초기화
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
       
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "AI 디지털 트랜스포메이션 뉴스레터 콘텐츠 생성 전문가. 간결하고 핵심적인 내용만 포함합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
       
        # 응답 처리
        content = response.choices[0].message.content
        return convert_markdown_to_html(content)
       
    except Exception as e:
        print(f"OpenAI API 오류: {str(e)}")
        # 상세 오류 정보 출력 (디버깅용)
        import traceback
        print(f"상세 오류 정보: {traceback.format_exc()}")
       
        # 오류 발생 시 기본 콘텐츠 반환
        default_contents = {
            'main_news': f"<p>OpenAI API 오류: 뉴스를 생성할 수 없습니다. (오류: {str(e)})</p>",
            'aidt_tips': get_default_tips_content(),
            'success_story': get_default_success_story(),
            'ai_use_case': get_default_ai_use_case()
        }
        return default_contents.get(content_type, f"<p>OpenAI API 오류: {str(e)}</p>")

def generate_git_lesson(openai_api_key, selected_week):
    """Git 학습 과정 섹션을 생성합니다."""
   
    # Git 주차별 학습 주제
    weekly_lessons = {
        "1주차": "Git 시작하기: 설치와 기본 개념 이해",
        "2주차": "저장소 생성과 기본 명령어: init, add, commit",
        "3주차": "브랜치 개념과 활용: branch, checkout, merge",
        "4주차": "원격 저장소 연동: remote, push, pull, clone",
        "5주차": "협업 워크플로우: fork, pull request, code review",
        "6주차": "충돌 해결과 히스토리 관리: merge conflict, rebase",
        "7주차": "고급 Git 기능: stash, cherry-pick, reset, revert",
        "8주차": "Git Flow와 브랜치 전략: feature, develop, release",
        "9주차": "GitHub/GitLab 활용: Issues, Projects, Actions",
        "10주차": "팀 협업 모범 사례: 커밋 메시지, 코드 리뷰 문화"
    }
   
    topic = weekly_lessons.get(selected_week, "해당 주차의 학습 내용이 없습니다.")
   
    # OpenAI API가 없는 경우 예외 처리
    if not openai_api_key:
        return f"""
        <div class="section">
            <div class="section-title">📚 차근차근 도전해보기 (Git 학습 과정)</div>
            <div class="section-container git-challenge">
                <h3>🛠 {selected_week}: {topic}</h3>
                <p>OpenAI API 키가 없어 상세 내용을 생성할 수 없습니다. API 키를 입력하시면 더 자세한 내용을 보실 수 있습니다.</p>
            </div>
        </div>
        """
   
    try:
        client = OpenAI(api_key=openai_api_key)
       
        prompt = f"""
        Git 학습 과정 {selected_week}의 주제는 "{topic}"입니다.
        다음 형식으로 웹 페이지 콘텐츠를 생성해주세요.
       
        1. 2-3개의 주요 섹션으로 나누어 설명해주세요. 각 섹션은 다음과 같은 형식으로 구성됩니다:
           - 섹션 제목 (예: "1. Git 개요", "주요 명령어" 등)
           - 각 섹션에는 명확하고 실용적인 3-4개의 핵심 요점을 포함해주세요.
           - 각 요점은 실제 Git 사용 시 도움이 되는 구체적인 정보여야 합니다.
       
        2. 마지막에는 5-8줄 정도의 실행 가능한 Git 명령어 예제를 포함해주세요.
           - 명령어는 실제로 작동하는 간단한 예제여야 합니다.
           - 해당 주차의 학습 내용을 실습할 수 있는 명령어를 작성해주세요.
           - 각 명령어에는 간단한 설명을 포함해주세요.
       
        응답은 반드시 JSON 형식으로 제공해주세요. 다음 JSON 형식을 정확히 따라야 합니다:
        {{
            "title": "제목 (간결하게)",
            "sections": [
                {{
                    "title": "섹션 제목 1",
                    "items": ["핵심 요점 1 (구체적이고 실용적인 내용)", "핵심 요점 2", "핵심 요점 3"]
                }},
                {{
                    "title": "섹션 제목 2",
                    "items": ["핵심 요점 1", "핵심 요점 2", "핵심 요점 3"]
                }}
            ],
            "example_commands": [
                {{
                    "command": "git 명령어",
                    "description": "명령어 설명"
                }}
            ]
        }}
        """
       
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Git 교육 전문가입니다. 학습 내용은 구체적이고 실용적이며 초보자도 이해하기 쉽게 작성합니다."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
       
        content = json.loads(response.choices[0].message.content)
       
        # HTML 섹션 생성
        sections_html = ""
        for section in content["sections"]:
            sections_html += f'<h4>💠 {section["title"]}</h4>\n'
           
            for item in section["items"]:
                sections_html += f'<p>✅ {item}</p>\n'
       
        # Git 명령어 예제 HTML
        commands_html = """
        <div class="code-example-box">
            <div class="code-example-title">실습 명령어</div>
            <div class="code-example-content">
        """
       
        for cmd in content["example_commands"]:
            commands_html += f"# {cmd['description']}\n{cmd['command']}\n\n"
       
        commands_html += """
            </div>
        </div>
        """
       
        # 전체 섹션 HTML
        section_html = f"""
        <div class="section">
            <div class="section-title">📚 차근차근 도전해보기 (Git 학습 과정)</div>
            <div class="section-container git-challenge">
                <h3>🛠 {selected_week}: {content["title"]}</h3>
                <div class="lesson-details">
                    {sections_html}
                </div>
                {commands_html}
            </div>
        </div>
        """
       
        return section_html
       
    except Exception as e:
        print(f"GPT API 오류: {str(e)}")
        return f"""
        <div class="section">
            <div class="section-title">📚 차근차근 도전해보기 (Git 학습 과정)</div>
            <div class="section-container git-challenge">
                <h3>🛠 {selected_week}: {topic}</h3>
                <p>OpenAI API 오류: {str(e)}</p>
                <p>API 키를 확인하시거나 잠시 후 다시 시도해주세요.</p>
            </div>
        </div>
        """

def generate_llm_lesson(openai_api_key, selected_week):
    """LLM 학습 과정 섹션을 생성합니다."""
   
    # LLM 주차별 학습 주제
    weekly_lessons = {
        "1주차": "LLM 기초: 대화형 AI의 원리와 ChatGPT 시작하기",
        "2주차": "효과적인 프롬프트 작성: 명확한 질문으로 좋은 답변 얻기",
        "3주차": "프롬프트 엔지니어링: Chain of Thought와 Few-shot Learning",
        "4주차": "업무별 활용법: 문서 작성, 번역, 요약 실습",
        "5주차": "창의적 작업: 브레인스토밍, 아이디어 발굴, 콘텐츠 생성",
        "6주차": "코딩 도우미: 프로그래밍 학습과 디버깅 활용",
        "7주차": "데이터 분석 지원: 엑셀 함수, 차트 해석, 보고서 작성",
        "8주차": "멀티모달 AI: 이미지, 음성과 함께하는 AI 활용",
        "9주차": "AI 도구 생태계: Claude, GPT, Gemini 비교 활용",
        "10주차": "AI 윤리와 미래: 책임감 있는 AI 사용법과 전망"
    }
   
    topic = weekly_lessons.get(selected_week, "해당 주차의 학습 내용이 없습니다.")
   
    # OpenAI API가 없는 경우 예외 처리
    if not openai_api_key:
        return f"""
        <div class="section">
            <div class="section-title">🤖 차근차근 도전해보기 (LLM 학습 과정)</div>
            <div class="section-container llm-challenge">
                <h3>📚 {selected_week}: {topic}</h3>
                <p>OpenAI API 키가 없어 상세 내용을 생성할 수 없습니다. API 키를 입력하시면 더 자세한 내용을 보실 수 있습니다.</p>
            </div>
        </div>
        """
   
    try:
        client = OpenAI(api_key=openai_api_key)
       
        prompt = f"""
        LLM 학습 과정 {selected_week}의 주제는 "{topic}"입니다.
        초보자도 쉽게 이해할 수 있도록 다음 형식으로 웹 페이지 콘텐츠를 생성해주세요.
       
        1. 3-4개의 주요 섹션으로 나누어 설명해주세요. 각 섹션은 다음과 같은 형식으로 구성됩니다:
           - 섹션 제목 (예: "1. LLM이란 무엇인가?", "기본 개념 이해하기" 등)
           - 각 섹션에는 명확하고 실용적인 3-4개의 핵심 요점을 포함해주세요.
           - 각 요점은 초보자가 이해하기 쉽도록 구체적인 예시와 함께 설명해주세요.
           - 일상생활이나 업무에서 바로 적용할 수 있는 실용적인 정보여야 합니다.
       
        2. 마지막에는 5-8개의 실제로 시도해볼 수 있는 프롬프트 예제를 포함해주세요.
           - 각 프롬프트는 해당 주차의 학습 내용을 실습할 수 있는 구체적인 예시여야 합니다.
           - 프롬프트와 함께 "이렇게 사용하세요" 형태의 설명을 포함해주세요.
           - 초보자가 따라하기 쉬운 단계별 설명을 제공하세요.
       
        응답은 반드시 JSON 형식으로 제공해주세요. 다음 JSON 형식을 정확히 따라야 합니다:
        {{
            "title": "제목 (간결하고 이해하기 쉽게)",
            "sections": [
                {{
                    "title": "섹션 제목 1",
                    "items": ["핵심 요점 1 (구체적인 예시 포함)", "핵심 요점 2", "핵심 요점 3", "핵심 요점 4"]
                }},
                {{
                    "title": "섹션 제목 2",
                    "items": ["핵심 요점 1", "핵심 요점 2", "핵심 요점 3"]
                }}
            ],
            "example_prompts": [
                {{
                    "prompt": "실제 사용할 수 있는 프롬프트 예시",
                    "description": "이 프롬프트 사용법과 기대 결과에 대한 자세한 설명"
                }}
            ]
        }}
        """
       
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "LLM 교육 전문가입니다. 학습 내용은 구체적이고 실용적이며 초보자도 이해하기 쉽게 작성합니다. 모든 설명에는 구체적인 예시를 포함하고, 실생활 활용법을 제시합니다."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
       
        content = json.loads(response.choices[0].message.content)
       
        # HTML 섹션 생성
        sections_html = ""
        for section in content["sections"]:
            sections_html += f'<h4>💡 {section["title"]}</h4>\n'
           
            for item in section["items"]:
                sections_html += f'<p>✅ {item}</p>\n'
       
        # 프롬프트 예제 HTML
        prompts_html = """
        <div class="code-example-box">
            <div class="code-example-title">실습 프롬프트 예제</div>
            <div class="code-example-content">
        """
       
        for i, prompt_data in enumerate(content["example_prompts"], 1):
            prompts_html += f"예제 {i}: {prompt_data['description']}\n"
            prompts_html += f"프롬프트: \"{prompt_data['prompt']}\"\n\n"
       
        prompts_html += """
            </div>
        </div>
        """
       
        # 전체 섹션 HTML
        section_html = f"""
        <div class="section">
            <div class="section-title">🤖 차근차근 도전해보기 (LLM 학습 과정)</div>
            <div class="section-container llm-challenge">
                <h3>📚 {selected_week}: {content["title"]}</h3>
                <div class="lesson-details">
                    {sections_html}
                </div>
                {prompts_html}
            </div>
        </div>
        """
       
        return section_html
       
    except Exception as e:
        print(f"GPT API 오류: {str(e)}")
        return f"""
        <div class="section">
            <div class="section-title">🤖 차근차근 도전해보기 (LLM 학습 과정)</div>
            <div class="section-container llm-challenge">
                <h3>📚 {selected_week}: {topic}</h3>
                <p>OpenAI API 오류: {str(e)}</p>
                <p>API 키를 확인하시거나 잠시 후 다시 시도해주세요.</p>
            </div>
        </div>
        """

def create_newsletter_html(content, issue_number, date, highlight_settings, git_section=""):
    """웹툰 스타일 뉴스레터 HTML 템플릿 생성 함수"""
    
    # 하이라이트 설정 기본값
    default_highlight = {
        "title": "시선이 바뀌면 세상이 달라집니다",
        "subtitle": "어제까지 당연하다고 생각했던 것들이 오늘은 왜 이렇게 이상해 보일까요? 🤔",
        "description": "답은 간단합니다.\n시선이 바뀌었기 때문입니다. 🔍",
        "link_text": "AT/DT 추진방향 →",
        "link_url": "#"
    }
    
    # 사용자 정의 하이라이트 설정 또는 기본값 사용
    highlight = {**default_highlight, **highlight_settings}
    
    # 웹툰 스타일 CSS
    css_styles = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
        
        body {
            font-family: 'Noto Sans KR', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 20px auto;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        /* 웹툰 스타일 헤더 */
        .header {
            background: linear-gradient(45deg, #2d3436, #636e72);
            color: white;
            padding: 20px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 3px solid #74b9ff;
        }
        
        .close-btn {
            font-size: 20px;
            cursor: pointer;
            opacity: 0.8;
        }
        
        .header-title {
            font-size: 20px;
            font-weight: 700;
            text-align: center;
            flex: 1;
            letter-spacing: 2px;
        }
        
        .logo {
            font-size: 14px;
            color: #74b9ff;
            font-weight: 700;
            background: white;
            padding: 5px 10px;
            border-radius: 15px;
        }
        
        /* 탭 섹션 */
        .tab-section {
            background: linear-gradient(45deg, #00d2ff, #3a7bd5);
            padding: 20px 30px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .tab-date {
            background: #7b68ee;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .tab-hashtags {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 500;
        }
        
        .newsletter-intro {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: white;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
        }
        
        /* 메인 히어로 섹션 */
        .hero-section {
            background: #ffd700;
            padding: 60px 50px;
            position: relative;
            min-height: 300px;
            display: flex;
            align-items: center;
        }
        
        .hero-content {
            flex: 1;
            z-index: 2;
        }
        
        .hero-title {
            font-size: 42px;
            font-weight: 900;
            color: #2d3436;
            line-height: 1.2;
            margin-bottom: 30px;
            border-bottom: 4px solid #2d3436;
            padding-bottom: 15px;
            display: inline-block;
        }
        
        .hero-character {
            position: absolute;
            right: 50px;
            top: 50%;
            transform: translateY(-50%);
            width: 180px;
            height: 180px;
            z-index: 1;
        }
        
        .hero-dialogue {
            background: rgba(255,255,255,0.9);
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            font-size: 16px;
            position: relative;
            border-left: 5px solid #ff6b6b;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        
        .hero-dialogue::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 30px;
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-bottom: 10px solid rgba(255,255,255,0.9);
        }
        
        .hero-conclusion {
            font-size: 24px;
            font-weight: 800;
            color: #2d3436;
            margin-top: 30px;
            text-align: center;
            background: rgba(255,255,255,0.8);
            padding: 20px;
            border-radius: 15px;
        }
        
        .hero-link {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 700;
            margin-top: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        
        .hero-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.3);
        }
        
        /* 콘텐츠 섹션들 */
        .content-section {
            padding: 40px 50px;
            position: relative;
            border-bottom: 5px solid #f0f0f0;
        }
        
        .section-global {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .section-domestic {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .section-tips {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        .section-case {
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: #2d3436;
        }
        
        .section-title {
            font-size: 32px;
            font-weight: 900;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
            border-bottom: 3px solid rgba(255,255,255,0.3);
            padding-bottom: 15px;
        }
        
        .section-case .section-title {
            border-bottom: 3px solid rgba(45,52,54,0.3);
        }
        
        .section-icon {
            font-size: 36px;
        }
        
        /* 뉴스 아이템 */
        .news-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 20px;
        }
        
        .news-item {
            background: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
            position: relative;
        }
        
        .news-item:hover {
            transform: translateY(-5px);
        }
        
        .section-global .news-item,
        .section-domestic .news-item,
        .section-tips .news-item {
            color: #2d3436;
        }
        
        .news-title {
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 15px;
            color: #2d3436;
            line-height: 1.3;
        }
        
        .news-content {
            font-size: 14px;
            line-height: 1.7;
            color: #636e72;
            margin-bottom: 15px;
        }
        
        .news-source {
            font-size: 12px;
            color: #74b9ff;
            font-weight: 600;
            background: #f8f9fa;
            padding: 5px 10px;
            border-radius: 10px;
            display: inline-block;
        }
        
        /* 팁 섹션 특별 스타일 - 기존 구성 완전히 유지 */
        .tips-container {
            background: rgba(255,255,255,0.95);
            padding: 35px;
            border-radius: 25px;
            color: #2d3436;
            margin-top: 20px;
        }
        
        .aidt-tips {
            font-size: 14px;
        }
        
        .aidt-tips .tip-title {
            background: linear-gradient(45deg, #ffecd2, #fcb69f);
            color: #2d3436;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 20px;
            text-align: center;
        }
        
        .aidt-tips .prompt-examples-title {
            background: linear-gradient(45deg, #fd79a8, #e84393);
            color: white;
            padding: 15px 20px;
            margin: 25px 0 20px 0;
            border-radius: 15px;
            font-weight: 700;
            font-size: 18px;
        }
        
        .aidt-tips .prompt-template {
            background: white;
            margin-bottom: 25px;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #74b9ff;
        }
        
        .aidt-tips .template-title {
            color: #2d3436;
            font-weight: 800;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .aidt-tips .template-content {
            margin-left: 0;
        }
        
        .aidt-tips .example-label, 
        .aidt-tips .prompt-label {
            font-weight: 700;
            margin-top: 15px;
            color: #6c5ce7;
            font-size: 14px;
        }
        
        .aidt-tips .example-content, 
        .aidt-tips .prompt-content {
            background: #f8f9fa;
            padding: 18px;
            border-radius: 12px;
            margin: 10px 0;
            line-height: 1.7;
            border-left: 4px solid #74b9ff;
            color: #2d3436;
        }
        
        .aidt-tips .tip-footer {
            margin-top: 25px;
            font-style: italic;
            color: #636e72;
            text-align: center;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 15px;
        }
        
        .aidt-tips p {
            margin: 15px 0;
            line-height: 1.7;
        }
        
        /* 말풍선 스타일 */
        .speech-bubble {
            background: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 25px;
            position: relative;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            color: #2d3436;
        }
        
        .speech-bubble::before {
            content: '';
            position: absolute;
            top: -12px;
            left: 40px;
            width: 0;
            height: 0;
            border-left: 12px solid transparent;
            border-right: 12px solid transparent;
            border-bottom: 12px solid rgba(255,255,255,0.95);
        }
        
        /* AI 활용사례 특별 레이아웃 */
        .case-item {
            background: rgba(255,255,255,0.95);
            padding: 35px;
            border-radius: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            margin-top: 20px;
        }
        
        .case-title {
            font-size: 24px;
            font-weight: 800;
            color: #2d3436;
            margin-bottom: 20px;
            text-align: center;
            background: linear-gradient(45deg, #a8e6cf, #88d8a3);
            padding: 15px;
            border-radius: 15px;
        }
        
        .case-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 25px 0;
        }
        
        .stat-item {
            text-align: center;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 15px;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: 900;
            color: #00b894;
        }
        
        .stat-label {
            font-size: 12px;
            color: #636e72;
            margin-top: 5px;
        }
        
        /* Git 학습 섹션 */
        .llm-challenge {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            border-radius: 25px;
            padding: 35px;
            border: none;
            color: white;
            margin-top: 20px;
        }
        
        .git-challenge h3 {
            color: #00b894;
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 800;
        }
        
        .lesson-details h4 {
            font-size: 20px;
            font-weight: 700;
            color: #2d3436;
            margin: 20px 0 15px 0;
        }
        
        .lesson-details p {
            background: rgba(255,255,255,0.8);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            line-height: 1.6;
        }
        
        /* 코드 예제 박스 */
        .code-example-box {
            background: #2d3436;
            border-radius: 15px;
            margin: 25px 0;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .code-example-title {
            background: linear-gradient(45deg, #00b894, #00cec9);
            color: white;
            padding: 15px 25px;
            font-weight: 700;
            font-size: 16px;
        }
        
        .code-example-content {
            padding: 25px;
            color: #a8e6cf;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        /* 푸터 */
        .footer {
            background: linear-gradient(45deg, #2d3436, #636e72);
            color: white;
            padding: 30px;
            text-align: center;
            font-size: 14px;
        }
        
        .footer p {
            margin: 8px 0;
            opacity: 0.9;
        }
        
        /* 애니메이션 */
        @keyframes float {
            0%, 100% { transform: translateY(-50%) translateX(0px); }
            50% { transform: translateY(-50%) translateX(-10px); }
        }
        
        .floating {
            animation: float 4s ease-in-out infinite;
        }
        
        /* 반응형 */
        @media (max-width: 900px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .news-container {
                grid-template-columns: 1fr;
            }
            
            .prompt-examples-grid {
                grid-template-columns: 1fr;
            }
            
            .case-stats {
                grid-template-columns: 1fr;
            }
            
            .hero-section {
                padding: 40px 30px;
                flex-direction: column;
                text-align: center;
            }
            
            .hero-character {
                position: static;
                transform: none;
                margin-top: 20px;
            }
            
            .content-section {
                padding: 30px 25px;
            }
            
            .section-title {
                font-size: 24px;
            }
            
            .hero-title {
                font-size: 32px;
            }
        }
    </style>
    """
    
    # 캐릭터 SVG 생성
    character_svg = """
    <svg width="180" height="180" viewBox="0 0 180 180">
        <!-- 몸체 -->
        <ellipse cx="90" cy="120" rx="35" ry="45" fill="#ffb347" stroke="#333" stroke-width="3"/>
        
        <!-- 머리 -->
        <circle cx="90" cy="70" r="35" fill="#ffb347" stroke="#333" stroke-width="3"/>
        
        <!-- 귀 -->
        <ellipse cx="70" cy="55" rx="12" ry="18" fill="#ffb347" stroke="#333" stroke-width="3"/>
        <ellipse cx="110" cy="55" rx="12" ry="18" fill="#ffb347" stroke="#333" stroke-width="3"/>
        
        <!-- 눈 -->
        <circle cx="80" cy="65" r="4" fill="#333"/>
        <circle cx="100" cy="65" r="4" fill="#333"/>
        
        <!-- 입 -->
        <path d="M 78 78 Q 90 88 102 78" stroke="#333" stroke-width="3" fill="none"/>
        
        <!-- 망원경 -->
        <rect x="110" y="55" width="30" height="8" fill="#4a90e2" stroke="#333" stroke-width="2" rx="4"/>
        <circle cx="140" cy="59" r="6" fill="#333"/>
        <circle cx="140" cy="59" r="4" fill="#74b9ff"/>
        
        <!-- 팔 -->
        <ellipse cx="60" cy="105" rx="8" ry="20" fill="#ffb347" stroke="#333" stroke-width="3"/>
        <ellipse cx="120" cy="100" rx="8" ry="20" fill="#ffb347" stroke="#333" stroke-width="3"/>
        
        <!-- 다리 -->
        <ellipse cx="75" cy="155" rx="8" ry="18" fill="#ffb347" stroke="#333" stroke-width="3"/>
        <ellipse cx="105" cy="155" rx="8" ry="18" fill="#ffb347" stroke="#333" stroke-width="3"/>
    </svg>
    """
    
    # HTML 구조 생성
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>중부Infra AT/DT Weekly - 제{issue_number}호</title>
        {css_styles}
    </head>
    <body>
        <div class="container">
            <!-- 웹툰 스타일 헤더 -->
            <div class="header">
                <div class="close-btn">✕</div>
                <div class="header-title">중부Infra AT/DT Weekly</div>
                <div class="logo">중부Infra</div>
            </div>
            
            <!-- 탭 섹션 -->
            <div class="tab-section">
                <div class="tab-date">{date} ✨ 제{issue_number}호</div>
                <div class="tab-hashtags">#AI혁신 #디지털트랜스포메이션 #스마트워크</div>
            </div>
            
            <!-- 뉴스레터 소개 -->
            <div class="newsletter-intro">
                <p>📢 중부Infra AT/DT 뉴스레터는 모두가 AI발전 속도에 뒤쳐지지 않고 업무에 적용할 수 있도록 가장 흥미로운 AI 활용법을 전합니다.</p>
            </div>
            
            <!-- 메인 히어로 섹션 -->
            <div class="hero-section">
                <div class="hero-content">
                    <div class="hero-title">{highlight['title'].replace(' ', '<br>')}</div>
                    
                    <div class="hero-dialogue">
                        "{highlight['subtitle']}"
                    </div>
                    
                    <p style="font-size: 18px; color: #2d3436; margin: 20px 0;">답은 간단합니다.</p>
                    
                    <div class="hero-conclusion">{highlight['description'].replace(chr(10), '<br>')}</div>
                    
                    <a href="{highlight['link_url']}" class="hero-link">{highlight['link_text']}</a>
                </div>
                
                <!-- 캐릭터 일러스트 -->
                <div class="hero-character floating">
                    {character_svg}
                </div>
            </div>
    """
    
    # 섹션 추가 함수
    def add_webtoon_section(title, section_key, icon, section_class=""):
        if section_key not in content:
            return ""
            
        section_content = content[section_key]
        
        if section_key == "aidt_tips":
            # AI 팁 섹션 - 기존 구성 유지하되 웹툰 스타일 적용
            return f"""
            <div class="content-section {section_class}">
                <div class="section-title">
                    <span class="section-icon">{icon}</span>
                    {title}
                </div>
                
                <div class="tips-container aidt-tips">
                    {section_content}
                </div>
            </div>
            """
        elif section_key in ["naver_news", "naver_trends"]:
            # 말풍선 스타일 국내 뉴스
            return f"""
            <div class="content-section {section_class}">
                <div class="section-title">
                    <span class="section-icon">{icon}</span>
                    {title}
                </div>
                
                <div class="speech-bubble">
                    {section_content}
                </div>
            </div>
            """
        elif section_key == "ai_use_case":
            # AI 활용사례 특별 처리
            return f"""
            <div class="content-section {section_class}">
                <div class="section-title">
                    <span class="section-icon">{icon}</span>
                    {title}
                </div>
                
                <div class="case-item">
                    {section_content}
                </div>
            </div>
            """
        else:
            # 일반 뉴스 섹션 (2열 그리드)
            return f"""
            <div class="content-section {section_class}">
                <div class="section-title">
                    <span class="section-icon">{icon}</span>
                    {title}
                </div>
                
                <div class="news-container">
                    {section_content}
                </div>
            </div>
            """
    
    # 각 섹션 추가
    html += add_webtoon_section("글로벌 AI 뉴스", "main_news", "🌍", "section-global")
    html += add_webtoon_section("국내 AI 뉴스", "naver_news", "🇰🇷", "section-domestic")
    html += add_webtoon_section("국내 AI 트렌드", "naver_trends", "📈", "section-domestic")
    html += add_webtoon_section("이번 주 AT/DT 팁", "aidt_tips", "💡", "section-tips")
    html += add_webtoon_section("AI 활용사례", "ai_use_case", "🚀", "section-case")
    
    # Git 학습 섹션 추가 (있는 경우)
    if git_section:
        html += git_section
    
    # 푸터 및 닫는 태그
    html += f"""
            <!-- 푸터 -->
            <div class="footer">
                <p>🎨 © {datetime.now().year} 중부Infra All rights reserved. | 뉴스레터 구독에 감사드립니다.</p>
                <p>💌 문의사항이나 제안이 있으시면 언제든지 연락해 주세요^^.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def create_download_link(html_content, filename):
    """HTML 콘텐츠를 다운로드할 수 있는 링크를 생성합니다."""
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display: inline-block; margin-top: 20px; padding: 15px 30px; background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; text-decoration: none; border-radius: 25px; font-weight: bold; box-shadow: 0 8px 20px rgba(0,0,0,0.2);">🎨 웹툰 스타일 뉴스레터 다운로드</a>'
    return href





def generate_newsletter(api_keys, settings, custom_content=None):
    """통합된 뉴스레터 생성 함수"""
   
    # API 키 추출
    openai_api_key = api_keys.get('openai')
    news_api_key = api_keys.get('news_api')
    naver_client_id = api_keys.get('naver_client_id')
    naver_client_secret = api_keys.get('naver_client_secret')
   
    # 설정 추출
    issue_number = settings.get('issue_number', 1)
    news_query_en = settings.get('news_query_en', 'AI digital transformation')
    news_query_ko = settings.get('news_query_ko', 'AI 디지털 트랜스포메이션')
    language = settings.get('language', 'en')
    selected_week = settings.get('selected_week')
    highlight_settings = settings.get('highlight_settings', {})
   
    # 현재 날짜
    date = datetime.now().strftime('%Y년 %m월 %d일')
   
    # 뉴스레터 콘텐츠를 저장할 딕셔너리
    newsletter_content = {}
   
    # 1. 글로벌 뉴스 데이터 수집 (NewsAPI)
    news_info = ""
    openai_news_info = ""
   
    if news_api_key:
        try:
            # 일반 AI 관련 뉴스
            news_articles = fetch_news(
                'newsapi',
                news_query_en,
                days=7,
                language=language,
                display=5,
                api_key=news_api_key
            )
           
            news_info = "최근 7일 내 수집된 실제 뉴스 기사:\n\n"
            for i, article in enumerate(news_articles):
                pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')).strftime('%Y년 %m월 %d일')
                news_info += f"{i+1}. 제목: {article['title']}\n"
                news_info += f"   날짜: {pub_date}\n"
                news_info += f"   요약: {article['description']}\n"
                news_info += f"   출처: {article['source']['name']}\n"
                news_info += f"   URL: {article['url']}\n\n"
           
            # OpenAI 관련 뉴스
            openai_articles = fetch_news(
                'newsapi',
                "OpenAI",
                days=7,
                language=language,
                display=3,
                api_key=news_api_key
            )
           
            openai_news_info = "최근 7일 내 수집된 OpenAI 관련 뉴스 기사:\n\n"
            for i, article in enumerate(openai_articles):
                pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')).strftime('%Y년 %m월 %d일')
                openai_news_info += f"{i+1}. 제목: {article['title']}\n"
                openai_news_info += f"   날짜: {pub_date}\n"
                openai_news_info += f"   요약: {article['description']}\n"
                openai_news_info += f"   출처: {article['source']['name']}\n"
                openai_news_info += f"   URL: {article['url']}\n\n"
        except Exception as e:
            print(f"뉴스 데이터 수집 오류: {str(e)}")
   
    # 2. AI 팁 주제 선택
    ai_tip_topics = [
        "효과적인 프롬프트 작성의 기본 원칙 (Chain of Thought, Chain of Draft)",
        "특정 업무별 최적의 프롬프트 템플릿",
        "AI를 활용한 데이터 분석 프롬프트 기법",
        "창의적 작업을 위한 AI 프롬프트 전략",
        "AI와 협업하여 문제 해결하기",
        "다양한 AI 도구 활용법 비교",
        "업무 자동화를 위한 AI 프롬프트 설계",
        "AI를 활용한 의사결정 지원 기법"
    ]
    current_topic = ai_tip_topics[(issue_number - 1) % len(ai_tip_topics)]
   
    # 3. OpenAI로 콘텐츠 생성
    if openai_api_key:
        # 글로벌 AI 뉴스 섹션 생성
        if news_api_key:
            newsletter_content['main_news'] = generate_ai_content(
                openai_api_key,
                'main_news',
                None,
                date=date,
                news_info=news_info,
                openai_news_info=openai_news_info
            )
        else:
            newsletter_content['main_news'] = "<p>News API 키가 제공되지 않아 글로벌 뉴스를 가져올 수 없습니다.</p>"
       
        # AI 팁 섹션 생성
        newsletter_content['aidt_tips'] = generate_ai_content(
            openai_api_key,
            'aidt_tips',
            None,
            current_topic=current_topic
        )
       
        # 사용자 정의 성공 사례가 있는 경우 사용, 없으면 생성
        if custom_content and 'success_story' in custom_content:
            newsletter_content['success_story'] = convert_markdown_to_html(custom_content['success_story'])
        else:
            newsletter_content['success_story'] = generate_ai_content(openai_api_key, 'success_story')
           
        # AI 활용사례 생성 - 실제 사례 중심으로 수정
        real_use_case_prompt = """
        AIDT Weekly 뉴스레터의 'AI 활용사례' 섹션을 생성해주세요.
       
        실제 기업이나 조직에서 성공적으로 구현한 AI 활용사례를 다음 형식으로 작성해주세요:
       
        ## [기업/조직명]의 [구체적인 AI 활용 분야] 사례
       
        **요약:** 해당 기업이 AI를 활용한 실제 사례의 배경과 중요성을 2-3문장으로 설명해주세요. 기업명, 산업 분야, 도입 시기 등 실제 정보를 포함하세요.
       
        **단계별 방법:**
        1. [첫 번째 단계 - 구체적인 기술과 접근 방식]
        2. [두 번째 단계 - 실제 구현 방법]
        3. [세 번째 단계 - 데이터 처리나 모델 학습 방법]
        4. [네 번째 단계 - 실제 운영 과정]
       
        **추천 프롬프트:** 이 활용사례를 응용할 때 사용할 수 있는 구체적이고 실용적인 프롬프트 예시를 작성해주세요.
       
        다음 중 한 분야에 초점을 맞춰 실제 사례를 작성해주세요:
        1. 제조업 - 품질 관리, 예측 유지보수, 공정 최적화
        2. 금융 - 사기 탐지, 고객 세분화, 리스크 평가
        3. 의료 - 진단 보조, 환자 모니터링, 의료 영상 분석
        4. 소매/유통 - 수요 예측, 개인화 추천, 재고 관리
        5. 고객 서비스 - 챗봇, 감성 분석, 업무 자동화
       
        반드시 실제 존재하는 기업과 검증된 사례를 바탕으로 작성해주세요. 구체적인 수치와 성과를 포함하세요.
        사용한 실제 AI 기술(예: 딥러닝, 자연어 처리, 컴퓨터 비전 등)도 명시하세요.
        마케팅적 과장이나 가상의 정보는 포함하지 마세요.
       
        내용은 마크다운 형식으로 작성해주세요.
        """
       
        # GPT로 AI 활용사례 직접 생성
        ai_use_case_content = generate_ai_content(
            openai_api_key,
            'ai_use_case',
            real_use_case_prompt
        )
       
        # 실제 참고 링크 추가
        ai_use_case_content += f"""
        <p style="text-align: right; margin-top: 15px;"><a href="https://www.accenture.com/us-en/insights/artificial-intelligence-index" target="_blank" style="color: #ff5722; text-decoration: none; font-weight: bold;">더 많은 AI 활용사례 보기 →</a></p>
        <p style="font-size: 8pt; text-align: right; color: #666;">출처: Accenture AI 리서치</p>
        """
       
        newsletter_content['ai_use_case'] = ai_use_case_content
    else:
        # OpenAI API가 없을 경우 기본 콘텐츠 사용
        newsletter_content['aidt_tips'] = get_default_tips_content()
        newsletter_content['success_story'] = get_default_success_story()
        newsletter_content['ai_use_case'] = get_default_ai_use_case()
        if news_api_key:
            newsletter_content['main_news'] = "<p>OpenAI API 키가 없어 뉴스 분석을 할 수 없습니다.</p>"
   
    # 4. 네이버 API로 국내 뉴스 수집 및 콘텐츠 생성
    if naver_client_id and naver_client_secret:
        try:
            # 네이버 AI 뉴스
            ai_news_items = fetch_news(
                'naver',
                news_query_ko,
                display=2,
                days=7,
                client_id=naver_client_id,
                client_secret=naver_client_secret
            )
           
            # 네이버 AI 트렌드 뉴스
            trend_news_items = fetch_news(
                'naver',
                "AI 트렌드",
                display=2,
                days=7,
                client_id=naver_client_id,
                client_secret=naver_client_secret
            )
           
            # 네이버 뉴스 콘텐츠 생성
            naver_news_content = create_naver_news_section(ai_news_items, "국내 AI 주요 소식")
            trend_news_content = create_naver_news_section(trend_news_items, "국내 AI 트렌드 소식")
           
            newsletter_content['naver_news'] = naver_news_content
            newsletter_content['naver_trends'] = trend_news_content
           
        except Exception as e:
            print(f"네이버 API 관련 오류: {str(e)}")
            newsletter_content['naver_news'] = f"<p>네이버 뉴스를 가져오는 중 오류가 발생했습니다.</p>"
            newsletter_content['naver_trends'] = f"<p>네이버 AI 트렌드 뉴스를 가져오는 중 오류가 발생했습니다.</p>"
   
    # 5. Git 학습 과정 추가 (선택된 경우)
    git_challenge_section = ""
    if selected_week and openai_api_key:
        # git_challenge_section = generate_git_lesson(openai_api_key, selected_week)
        llm_challenge_section = generate_llm_lesson(openai_api_key, selected_week)
   
    # 6. HTML 템플릿 생성
    html_content = create_newsletter_html(
        newsletter_content,
        issue_number,
        date,
        highlight_settings,
        git_challenge_section
    )
   
    return html_content

# Streamlit 메인 함수
def main():
    st.set_page_config(
        page_title="🌟 중부Infra AT/DT Weekly 생성기",
        page_icon="🎨",
        layout="wide"
    )
    
    # 컬러풀한 헤더
    st.markdown("""
    <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24, #fd79a8); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            🎨 중부Infra AT/DT Weekly 생성기 ✨
        </h1>
        <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;">
            AI와 API를 활용하여 시각적이고 매력적인 뉴스레터를 자동으로 생성합니다 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바에 API 키 설정 섹션 배치하여 UI 개선
    with st.sidebar:
        st.markdown("### 🔑 API 키 설정")
        st.info("💡 사용 가능한 API 키만 입력하세요. 없는 API는 기본 콘텐츠로 대체됩니다.")
        
        openai_api_key = st.text_input("🤖 OpenAI API 키", type="password")
        news_api_key = st.text_input("📰 News API 키", type="password")
        naver_client_id = st.text_input("🇰🇷 네이버 Client ID", type="password")
        naver_client_secret = st.text_input("🔐 네이버 Client Secret", type="password")
    
    # 탭을 사용하여 설정 구성
    tab1, tab2, tab3 = st.tabs(["⚙️ 기본 설정", "🎨 디자인 설정", "📚 고급 설정"])
    
    with tab1:
        # 뉴스레터 기본 설정
        st.markdown("### 📋 뉴스레터 설정")
        
        issue_number = st.number_input("📄 뉴스레터 호수", min_value=1, value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            news_query_en = st.text_input(
                "🌍 NewsAPI 검색어 (영어)",
                value="Telecommunication AND AI digital transformation OR 5G OR 6G",
                help="뉴스 API 검색어 (AND, OR 연산자 사용 가능)"
            )
            
            language = st.selectbox(
                "🗣️ NewsAPI 언어",
                options=["en", "ko", "ja", "zh", "fr", "de"],
                format_func=lambda x: {"en": "🇺🇸 영어", "ko": "🇰🇷 한국어", "ja": "🇯🇵 일본어", 
                                     "zh": "🇨🇳 중국어", "fr": "🇫🇷 프랑스어", "de": "🇩🇪 독일어"}[x]
            )
        
        with col2:
            news_query_ko = st.text_input(
                "🇰🇷 네이버 검색어 (한글)",
                value="AI통신인공지능 디지털 트랜스포메이션"
            )
            
            selected_week = st.selectbox(
                "🤖 LLM 학습 주차",
                options=["1주차", "2주차", "3주차", "4주차", "5주차", 
                        "6주차", "7주차", "8주차", "9주차", "10주차"]
            )
    
    with tab2:
        # 하이라이트 박스 설정
        st.markdown("### 🌟 하이라이트 설정")
        
        # 미리 정의된 템플릿 선택
        template_options = get_highlight_suggestions()
        template_choice = st.selectbox(
            "🎨 템플릿 선택",
            options=range(len(template_options)),
            format_func=lambda x: f"템플릿 {x+1}: {template_options[x]['title'][:20]}..."
        )
        
        selected_template = template_options[template_choice]
        
        # 사용자 정의 가능
        col1, col2 = st.columns(2)
        with col1:
            highlight_title = st.text_input("✨ 하이라이트 제목", 
                                          value=selected_template["title"])
            highlight_subtitle = st.text_input("💭 하이라이트 부제목", 
                                             value=selected_template["subtitle"])
        
        with col2:
            highlight_description = st.text_area("📝 설명 텍스트", 
                                                value=selected_template["description"])
            
        col3, col4 = st.columns(2)
        with col3:
            highlight_link_text = st.text_input("🔗 링크 텍스트", value="AT/DT 추진방향 →")
        with col4:
            highlight_link_url = st.text_input("🌐 링크 URL", value="#")
    
    with tab3:
        # 성공 사례 커스텀 입력 옵션 추가
        st.markdown("### 🏆 성공 사례 설정 (선택사항)")
        custom_success_story = st.text_area(
            "📖 직접 작성한 성공 사례 (마크다운 형식)",
            value="",
            help="입력하지 않으면 AI가 자동으로 생성합니다. 마크다운 형식으로 입력하세요.",
            height=200
        )
    
    # 뉴스레터 생성 버튼 - 메인 영역에 배치
    if st.button("🚀 뉴스레터 생성", type="primary", use_container_width=True):
        # API 키 유효성 검사
        if not openai_api_key and (not naver_client_id or not naver_client_secret):
            st.error("❌ 최소한 OpenAI API 키 또는 네이버 API 키(Client ID + Client Secret) 중 하나는 입력해야 합니다.")
            return
        
        # 경고 메시지 표시
        warnings = []
        if not openai_api_key:
            warnings.append("🤖 OpenAI API 키가 없어 AI 생성 기능이 제한됩니다.")
        if not news_api_key:
            warnings.append("📰 News API 키가 없어 글로벌 뉴스 검색 기능이 제한됩니다.")
        if not naver_client_id or not naver_client_secret:
            warnings.append("🇰🇷 네이버 API 키가 없어 국내 뉴스 검색 기능이 제한됩니다.")
        
        if warnings:
            for warning in warnings:
                st.warning(warning)
        
        # 로딩 표시 및 뉴스레터 생성
        with st.spinner("🎨 뉴스레터 생성 중... (약 1-2분 소요될 수 있습니다)"):
            try:
                # API 키 딕셔너리 구성
                api_keys = {
                    'openai': openai_api_key,
                    'news_api': news_api_key,
                    'naver_client_id': naver_client_id,
                    'naver_client_secret': naver_client_secret
                }
                
                # 뉴스레터 설정 딕셔너리 구성
                settings = {
                    'issue_number': issue_number,
                    'news_query_en': news_query_en,
                    'news_query_ko': news_query_ko,
                    'language': language,
                    'selected_week': selected_week,
                    'highlight_settings': {
                        'title': highlight_title,
                        'subtitle': highlight_subtitle,
                        'description': highlight_description,
                        'link_text': highlight_link_text,
                        'link_url': highlight_link_url
                    }
                }
                
                # 사용자 정의 콘텐츠 딕셔너리
                custom_content = {}
                if custom_success_story:
                    custom_content['success_story'] = custom_success_story
                
                # 뉴스레터 생성
                newsletter_html = generate_newsletter(api_keys, settings, custom_content)
                
                # 결과 표시
                filename = f"중부Infra_ATDT_Weekly-제{issue_number}호.html"
                
                st.success(f"✅ 뉴스레터가 성공적으로 생성되었습니다! ({selected_week} Git 학습과정 포함)")
                st.markdown(create_download_link(newsletter_html, filename), unsafe_allow_html=True)
                
                # 미리보기 표시
                with st.expander("👀 뉴스레터 미리보기", expanded=True):
                    st.components.v1.html(newsletter_html, height=800, scrolling=True)
                
            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                st.error("🔍 자세한 오류 정보:")
                st.code(traceback.format_exc())

    # 도움말 표시
    with st.expander("💡 도움말 및 정보", expanded=False):
        st.markdown("""
        ### 🎨 중부Infra AT/DT Weekly 생성기 사용법

        1. **API 키 설정**: 사이드바에서 사용할 API 키를 입력합니다. 모든 키가 필요하지는 않습니다.
        2. **기본 설정**: 뉴스레터 호수, 검색어, 언어, Git 학습 주차를 설정합니다.
        3. **디자인 설정**: 하이라이트 박스 내용을 미리 준비된 템플릿 중에서 선택하거나 직접 커스터마이징할 수 있습니다.
        4. **고급 설정**: 성공 사례를 직접 작성할 수 있습니다.
        5. **뉴스레터 생성**: 설정이 완료되면 '뉴스레터 생성' 버튼을 클릭합니다.

        생성된 뉴스레터는 HTML 파일로 다운로드하거나 미리보기로 확인할 수 있습니다.

        ### 🔑 사용 API 정보

        - **OpenAI API**: AI 콘텐츠 생성 (뉴스 요약, AI 팁, 성공 사례 등)
        - **News API**: 글로벌 AI 뉴스 검색
        - **네이버 API**: 국내 AI 뉴스 및 블로그 검색

        각 API에 대한 키는 해당 서비스 사이트에서 발급받을 수 있습니다.

        ### 📚 Git 학습 과정 안내

        - **1주차**: Git 기본 개념과 설치
        - **2주차**: 기본 명령어 (add, commit, push)
        - **3주차**: 브랜치와 머지
        - **4주차**: 원격 저장소 활용
        - **5주차**: 협업 워크플로우
        - **6주차**: 충돌 해결
        - **7주차**: 고급 Git 기능
        - **8주차**: Git Flow 전략
        - **9주차**: GitHub/GitLab 활용
        - **10주차**: 팀 협업 모범 사례

        ### 🎨 디자인 특징

        - **컬러풀한 그라데이션**: 각 섹션마다 다른 색상 테마
        - **인터랙티브 요소**: 호버 효과와 애니메이션
        - **반응형 디자인**: 모바일과 데스크톱 모두 지원
        - **캐릭터 이모지**: 친근하고 재미있는 시각적 요소
        """)

if __name__ == "__main__":
    main()
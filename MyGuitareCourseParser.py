#!/usr/bin/env python3

import requests
import Constants

VIDEO_BASE_URL    = ''



COURSE_MODULES_URL = '/course-modules/'
LESSONS_URL       = '/lessons/'


response = requests.get(
  Constants.API_BASE_URL + Constants.COURSE_NAME,
  headers = {
    'Accept': 'application/json',
    'authorization': 'Bearer ' + Constants.API_BEARER
  }
)

if response.status_code == 200:
  json_response = response.json()

  courseModule_slug = ''
  userCourseModuleLesson_slug = ''

  """
  for userCourseModule in json_response['data']['userCourseModules']['data']:
    courseModule_slug = userCourseModule['courseModule']['data']['slug']
    for userCourseModuleLesson in userCourseModule['userCourseModuleLessons']['data']:
      userCourseModuleLesson_slug = userCourseModuleLesson['lesson']['data']['slug']

      lesson_url = API_BASE_URL + COURSE_NAME + COURSE_MODULES_URL + courseModule_slug + LESSONS_URL + userCourseModuleLesson_slug
      
      response = requests.patch(
        lesson_url,
        headers = {
          'Accept': 'application/json',
          'authorization': 'Bearer ' + API_BEARER
        },
        params = {'action': 'start'},
      )
      if response.status_code == 200:
        json_response = response.json()

        lesson_title = str(json_response['data']['position']).zfill(2) + '_' + json_response['data']['lesson']['data']['title'].replace(' ', '_')

        for video in json_response['data']['lesson']['data']['lessonParts']['data']:
          video_title = str(video['position']).zfill(2) + '_' + video['title'].replace(' ', '_')
          video_url = VIMEO_BASE_URL + video['video_id']

          response = requests.get(
            video_url,
            headers = {
              'Referer': lesson_url
            }
          )
          if response.status_code == 200:
            text_response = response.text

            end_url_str = 'master.json?base64_init=1'
            end_url = text_response.rfind(end_url_str, 0, len(text_response))
            start_url = text_response.rfind('https', 0, end_url)

            video_cdn_url = text_response[start_url:end_url + len(end_url_str)]

            print(video_cdn_url + ',' + lesson_title + '/' + video_title)
          else:
            print(str(response.status_code) + ' ' + video_url)
      elif response.status_code == 403:
        print(str(response.status_code) + ' ' + lesson_url)
        break
      else:
        print(str(response.status_code) + ' ' + lesson_url)
      """
else:
  print(str(response.status_code) + ' GET ' + Constants.API_BASE_URL + Constants.COURSE_NAME)


#!/usr/bin/env python3

import requests
import Constants

COURSE_MODULES_URL = '/course-modules/'
LESSONS_URL       = '/lessons/'



output_file = open('links.txt', 'w')

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
  
  for userCourseModule in json_response['data']['userCourseModules']['data']:
    courseModule_slug = userCourseModule['courseModule']['data']['slug']
    for userCourseModuleLesson in userCourseModule['userCourseModuleLessons']['data']:
      userCourseModuleLesson_slug = userCourseModuleLesson['lesson']['data']['slug']

      lesson_url = Constants.API_BASE_URL + Constants.COURSE_NAME + COURSE_MODULES_URL + courseModule_slug + LESSONS_URL + userCourseModuleLesson_slug
      
      response = requests.patch(
        lesson_url,
        headers = {
          'Accept': 'application/json',
          'authorization': 'Bearer ' + Constants.API_BEARER
        },
        params = {'action': 'start'},
      )
      if response.status_code == 200:
        json_response = response.json()
        
        lesson_title = str(json_response['data']['position']).zfill(2) + '_' + json_response['data']['lesson']['data']['title'].replace(' ', '_')

        for video in json_response['data']['lesson']['data']['lessonParts']['data']:
          video_title = str(video['position']).zfill(2) + '_' + video['title'].replace(' ', '_')
          video_url = Constants.VIMEO_BASE_URL + video['video_id']
          
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

            output_file.write('python3 ' + Constants.VIMEO_DOWNLOAD_PATH + ' --url ' + video_cdn_url + ' --output ' + Constants.COURSE_NAME.replace('-', '_') + '/'+ lesson_title + '/' + video_title + ' --destination ' + Constants.VIDEO_DOWNLOAD_DST + '\n')
          else:
            print(str(response.status_code) + ' GET ' + video_url)
      
        # tablatures
        lesson_tablatures_url = Constants.API_BASE_URL + Constants.COURSE_NAME + COURSE_MODULES_URL + courseModule_slug + LESSONS_URL + userCourseModuleLesson_slug + '/tablatures'   

        response = requests.get(
          lesson_tablatures_url,
          headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer ' + Constants.API_BEARER
          }
        )
        if response.status_code == 200:
          json_tablatures_response = response.json()
          for tablature in json_tablatures_response['data']:
            output_file.write('wget ' + tablature['link'] + ' -P ' + Constants.VIDEO_DOWNLOAD_DST + Constants.COURSE_NAME.replace('-', '_') + '/'+ lesson_title + '/tablatures/' + '\n')
        else:
          print(str(response.status_code) + ' GET ' + lesson_tablatures_url)

        # resources
        lesson_resources_url = Constants.API_BASE_URL + Constants.COURSE_NAME + COURSE_MODULES_URL + courseModule_slug + LESSONS_URL + userCourseModuleLesson_slug + '/resources'   

        response = requests.get(
          lesson_resources_url,
          headers = {
            'Accept': 'application/json',
            'authorization': 'Bearer ' + Constants.API_BEARER
          }
        )
        if response.status_code == 200:
          json_resources_response = response.json()
          for resource in json_resources_response['data']:
            output_file.write('wget ' + resource['link'] + ' -P ' + Constants.VIDEO_DOWNLOAD_DST + Constants.COURSE_NAME.replace('-', '_') + '/'+ lesson_title + '/resources/' + '\n')
        else:
          print(str(response.status_code) + ' GET ' + lesson_resources_url)


      elif response.status_code == 403:
        print(str(response.status_code) + ' PATCH ' + lesson_url)
        break
      else:
        print(str(response.status_code) + ' PATCH ' + lesson_url)
else:
  print(str(response.status_code) + ' GET ' + Constants.API_BASE_URL + Constants.COURSE_NAME)

output_file.close()
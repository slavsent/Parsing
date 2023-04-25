from pymongo import MongoClient
from lesson_2_1 import jobs_hh, jobs_suoperjob
from pprint import pprint

client = MongoClient()
db = client.db_job


def add_in_base(job_name='elektrik', pages=0):
    base_hh = jobs_hh(job_name, pages)

    for el_job in base_hh.values():
        if len(list(db.jobs.find({'link-jobs': el_job['link-jobs']}))) == 0:
            db.jobs.insert_one(
                {
                    'link-jobs': el_job['link-jobs'],
                    'name': el_job['name'],
                    'salary_max': (0 if el_job['salary_max'] == '' else int(el_job['salary_max'])),
                    'salary_min': (0 if el_job['salary_min'] == '' else int(el_job['salary_min'])),
                    'site_job': el_job['site_job']
                }
            )

    base_jobs = jobs_suoperjob(job_name, pages)

    for el_job in base_jobs.values():
        if len(list(db.jobs.find({'link-jobs': el_job['link-jobs']}))) == 0:
            db.jobs.insert_one(
                {
                    'link-jobs': el_job['link-jobs'],
                    'name': el_job['name'],
                    'salary_max': (0 if el_job['salary_max'] == '' else int(el_job['salary_max'])),
                    'salary_min': (0 if el_job['salary_min'] == '' else int(el_job['salary_min'])),
                    'site_job': el_job['site_job']
                }
            )

    for el in db.jobs.find():
        pprint(el)


def find_salary_jobs(salary=0):
    find_jobs = db.jobs.find({'$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]})
    return find_jobs


def find_salary_jobs_other(salary=0):
    for el in db.jobs.find():
        if el['salary_min'] >= salary or el['salary_max'] >= salary:
            db.jobs_find.insert_one(el)


if __name__ == '__main__':
    if len(list(db.jobs.find())) > 0:
        db.jobs.drop()
    add_in_base('elektrik', 0)
    print(len(list(db.jobs.find())))

    if len(list(db.jobs_find.find())) > 0:
        db.jobs_find.drop()
    find_salary_jobs_other(50000)
    for el in db.jobs_find.find():
        pprint(el)
    print(len(list(db.jobs_find.find())))
    print(len(list(find_salary_jobs(50000))))
    for el in find_salary_jobs(50000):
        pprint(el)

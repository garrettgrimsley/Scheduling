# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class ConstraintSatisfactionPipeline(object):
    def process_item(self, item, spider):
        if item["course_reference_number"]:
                if item["time_start"] and item["time_end"]:
                    return item
        else:
            raise DropItem("Missing CRN in %s" % item)


class ConstraintSatisfactionPipelineHasDays(object):
    def process_item(self, item, spider):
        if item["days"]:
            return item
        else:
            raise DropItem("Missing days in %s" % item)

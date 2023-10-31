from pydantic import BaseModel, Field, root_validator
from pydantic.validators import datetime


class JournalistsByCountry(BaseModel):
    alpha2_code: str
    country_name: str
    users_count: int


class UsersByGroup(BaseModel):
    group_id: int
    group_name: str
    users_count: int


class TopicsByCountry(BaseModel):
    alpha2_code: str
    country_name: str
    topics_count: int


class TopicsByJournalist(BaseModel):
    username: str
    topics_count: int


class TopicsByTimeChunk(BaseModel):
    date_start: datetime
    topics_count: int


class PeriodsOfYears(BaseModel):
    year_start: int | None = None
    year_end: int | None = None

    @root_validator
    def validate_years(cls, values):
        _year_start = values.get("year_start")
        _year_end = values.get("year_end")
        if _year_start and _year_end:
            values["year_start"] = min(_year_start, _year_end)
            values["year_end"] = max(_year_start, _year_end)
        return values


class PeriodsOfYearsAndMonth(PeriodsOfYears):
    month: int | None = Field(
        None, ge=1, le=12, description="The value must be in the range from 1 to 12"
    )


class UserSalaryFilterYears(BaseModel):
    p_user_id: int | None = None
    p_created_by_user_id: int | None = None
    p_year_start: int | None = None
    p_year_end: int | None = None
    p_skip_empty_salary_info: bool = True


class UserSalaryFilterYearsAndMonth(UserSalaryFilterYears):
    p_month: int | None = None


class UserSalaryManagerFilterYear(BaseModel):
    p_user_id: int
    p_year_start: int | None = None
    p_year_end: int | None = None


class UserSalaryManagerFilterMonth(UserSalaryManagerFilterYear):
    p_month: int | None = Field(
        None, ge=1, le=12, description="The value must be in the range from 1 to 12"
    )


class UserSalaryFilterPaginated(BaseModel):
    p_user_name: str | None = None
    p_country_name: str | None = None
    p_amount_from: int | None = None
    p_amount_to: int | None = None
    p_month: int | None = None
    p_year: int | None = None
    p_added_by_username: str | None = None

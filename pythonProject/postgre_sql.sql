select
sitt.sqdh as ORD_NO,
sitt.barcode as SAMP_NO,
sitt.test_code,
sitt.test_project as TEST_ITEM,
sitt.test_project_detail as test_dtl,
sitt.teststarttime as test_start_time,
(case when position('充电' in sitt.step_type)>0 then '充电'
  when position('放电' in sitt.step_type)>0 then '放电' else null end )as TYP,
sitt.stepnum as step_no,
sitt.mea_rate as mes_RATE,
tridi.steptime as test_time,
tridi.voltage as INSTANTANEOUS_V,
ABS(tridi."Current"*tridi.steptime/3600)as INSTANTANEOUS_CAP
from
(select * from tvc_report_interm_step_data where mea_rate>0.1) sitt
left join tvc_report_interm_detail_info_data tridi
on tridi.barcode = sitt.barcode
and tridi.StepNum = sitt.stepnum
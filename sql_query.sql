SELECT [RayStationPatientDB_Clinical2025].[dbo].[RS_Patient_6].[PatientID_6_660]
            ,[RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Name_1550_1577]
            --,[RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Id]
            --,[RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[ApprovalStatus_1661_1662]
            --,[RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[ReviewTime_1661_1665]
            --,[RayStationPatientDB_Clinical2025].[dbo].[RS_RadiationSet_1553].[DicomPlanLabel_1553_1684]
        FROM [RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550]

        LEFT JOIN [RayStationPatientDB_Clinical2025].[dbo].[RS_Patient_6] ON [RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[AggregateId_] = [RayStationPatientDB_Clinical2025].[dbo].[RS_Patient_6].[AggregateId_]
        LEFT JOIN [RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661] ON  [RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[AggregateId_] = [RayStationPatientDB_Clinical2025].[dbo].[RS_Patient_6].[AggregateId_] 
        LEFT JOIN [RayStationPatientDB_Clinical2025].[dbo].[RS_RadiationSet_1553] ON concat([RayStationPatientDB_Clinical2025].[dbo].[RS_RadiationSet_1553].[ParentId_1731_1732],[RayStationPatientDB_Clinical2025].[dbo].[RS_RadiationSet_1553].[ParentId_1431_1737],[RayStationPatientDB_Clinical2025].[dbo].[RS_RadiationSet_1553].[ParentId_1550_1555]) = [RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Id]
        WHERE CONCAT([ParentId_1553_1666],[ParentId_1360_10514],[ParentId_1368_10517],[ParentId_1550_1667],[ParentId_2709_2710],[ParentId_9694_9698],[ParentId_11002_11005],[ParentId_11004_11007],[ParentId_11600_11613])  = [RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Id] 
        AND [RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[ApprovalStatus_1661_1662] NOT LIKE  '%Unapproved%'
        --CHANGE TO DATE BELOW
        AND [RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[ReviewTime_1661_1665] <= GETDATE()
        AND --CHANGE SITES AS NEEDED BELOW--
                UPPER([RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Name_1550_1577]) LIKE '%TOMO%'
  AND UPPER([RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Name_1550_1577]) NOT LIKE '%DNU%'
  AND UPPER([RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Name_1550_1577]) NOT LIKE '%ZZZ%'
  AND UPPER([RayStationPatientDB_Clinical2025].[dbo].[RS_TreatmentPlan_1550].[Name_1550_1577]) NOT LIKE '%E2E%'
        ORDER BY [RayStationPatientDB_Clinical2025].[dbo].[RS_Review_1661].[ReviewTime_1661_1665] ASC

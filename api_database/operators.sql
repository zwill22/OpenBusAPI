SELECT  NOCCODE,
                 OperatorPublicName,
                 PubNmId,
                 MAX(Mode) AS Mode,
                 TTRteEnq,
                 FareEnq,
                 ComplEnq,
                 Twitter,
                 Website
FROM (SELECT DISTINCT NOCCODE,
                      OperatorPublicName,
                      PubNmId,
                      Mode,
                      TTRteEnq,
                      FareEnq,
                      ComplEnq,
                      Twitter,
                      Website
      FROM NOCTable
               INNER JOIN PublicName USING (PubNmId, OperatorPublicName)
               LEFT JOIN (SELECT DISTINCT NOCCODE, PubNm, RefNm, Mode
                          FROM NOCLines) USING (NOCCODE))
GROUP BY NOCCODE, OperatorPublicName, PubNmId, TTRteEnq, FareEnq, ComplEnq, Twitter, Website
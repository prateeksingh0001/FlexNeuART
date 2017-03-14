#!/bin/bash
. scripts/common.sh
col="squad"
query_qty="2500"

USE_ALTERN_PIVOT_DIST=0

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 200 "9 11 13 15 17 19 21 23 25 27 29" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 200 ... "

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 100 "3 5 7 9 13 15 17 19 21 23 25" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 100 ... "

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 50 "3 4 5 6 7 8 9 10" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 50 ... "

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 25 "2 3 4 5 6 7 8 9" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 25 ... "

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 10 "1 2 3 4 5 6 7 8" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 10 ... "

../../knn4qa/tune_napp_exper1.sh $col $USE_ALTERN_PIVOT_DIST 5 "1 2 3 4 5 6 7 8" $query_qty
check "../../knn4qa/tune_napp_exper1.sh $col 5 ... "


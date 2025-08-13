args <- commandArgs(trailingOnly = TRUE)
setwd(args[1])  # result/<folder> を作業ディレクトリに設定

# 関数スクリプトを読み込み（絶対パスにするか相対パスに注意）
source("../../source_r/centreScaleDiagrams.R")
source("../../source_r/distanceMatrix.R")
source("../../source_r/extendedPersistence.R")
source("../../source_r/extractBoundary.R")
source("../../source_r/plot.extendedPHT.R")

library(imager)

for (k in 0:29){
  img <- load.image(paste("rot_",k,"_30.png", sep = ""))
  img = 1 - img
  boundaryAirway <- extractBoundary(img)
  xphtAirway <- extendedPersistence(boundaryAirway, 'branch', 36)
  centredAirway <- centreScaleDiagrams(xphtAirway, scale = FALSE)

  for (i in 1:length(centredAirway)){
    write.table(
      centredAirway[[i]]$Rel1,
      paste("rot_",k,"_30_rel",i,".txt", sep = ""),
      col.names = FALSE,
      row.names = FALSE
    )
  }
}

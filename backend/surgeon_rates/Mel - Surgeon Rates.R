
# Description: Surgeon Rates file for the Melanoma project

#-------------------
#  Workspace setup
#-------------------

rm(list = ls())

# Load previous workspace
setwd("O:/Outcomes/Andrew/Amplio/Services/Surgery/Gastric_and_MixedTumor/Melanoma")
load("Results/AllData_new.RData")

# Initialize the dataframe where the final results will be stored
userResults <- NULL 

# Add the SelectCohort Function
source(paste0(getwd(), "/Code/Mel - SelectCohort.R"))

# Resource analytic functions
source("O:/Outcomes/Andrew/Amplio/Functions/Production/ImportAnalyticFunctions.R")
source("O:/Outcomes/Andrew/Amplio/Functions/ryanw/SourceUpdatedFunctions.R")

# Add necessary libraries
library(dplyr)
#library(lattice)

# Remove tidyr if loaded in workspace 
# (this is because function "complete" overloads function used in mice package)
if ("package:tidyr" %in% search()) {
  detach("package:tidyr", unload = TRUE)
}


# FH: this value isn't initialized and looks like it's commented out everywhere else
# convert site to factor
# z <- unique(AllData$site)
# z <- z[!is.na(z)]
# 
# AllData$site <- factor(AllData$site, labels = z)

# Use the multiple imputation function to impute all covariates
imputedValues <- GenerateMultipleImputations(df = AllData, 
                                             vars = c("age", "female", "bmi", 
                                                      "thickness", 'ulceration'),  
                                             # TODO: add back in: "mitoticIndex" 
                                             patientId = "eventId")

# not using categoriacal thickness anymore
# # Create any necessary variables based on the imputations
# imputedValues <- lapply(imputedValues, function(x) {
#   
#   # melanoma on trunk, arm, or leg
#   x$siteCat1 <- as.numeric(grepl("TRUNK|ARM|LEG", x$site))
#   x$siteCat1[is.na(x$siteCat1)] <- NA
#   
#   # melanoma on scalp, neck, hand, foot
#   x$siteCat2 <- as.numeric(grepl("SCALP|NECK|HAND|FOOT", x$site))
#   x$siteCat2[is.na(x$siteCat2)] <- NA
#   
#   # melanoma on face, ear, eyelid, lip, or occular and mucosal sites
#   x$siteCat3 <- as.numeric(grepl("FACE|EAR|OCULAR|EYELID|LIP|MUCOSAL", x$site)) 
#   x$siteCat3[is.na(x$siteCat3)] <- NA
#   
#   return(x)
# })
# stopifnot(length(unique(imputedValues[[1]]$siteCat2)) == 2)

# Risk groups
riskGroups <- ReturnProcRiskGroups("Mel")


# Remove tbl_df class added by dplyr groupings
AllData <- as.data.frame(AllData)

# Generate date ids for slider
dateIds <- GenerateDateIds(AllData, "surgDate")

dateIds <- as.vector(outer(c("ALLLENGTH.", "LESSTHANPT8MM.", "PT8MMTO1MM.", 
                             "GRTHAN1MM."), dateIds, paste0))

# Covariates for wide excision outcomes
#wideExcisionCovs <- c("ageCat", "bmi", "siteCat2", "siteCat3", "thickCat") 
# TODO: add back in: "highASA", 
wideExcisionCovs <- c("age", "female", "bmi", "thickness", "ulceration" ) 
# TODO: add back in: "highASA", "mitoticIndex"


#------------
#  Outcomes
#------------


#### Complications
# Create model id

# Complication types
compTypes <- c("ANY.", "WOUND.", "CELLULITIS.", "SEROMA.", "GRAFT.") 
# note G2W is in db
compGrades <- c("COMPGRADE2.", "COMPGRADE3.")

compIds <- as.vector(outer(compTypes, compGrades, paste0))

compModelIdTemp <- as.vector(outer(compIds, dateIds, paste0))
compModelId <- paste0("COMP.", compModelIdTemp)

# Outcome id
outcomeId <- NULL

# Looping over all model IDs to obtain the rates for each model               
for (i in 1:length(compModelId)) {
  print(compModelId[i])    
  
  if (length(grep("ANY.COMPGRADE2.", compModelId[i])) > 0) {
    outcomeId <- "anyComp2"
  }
  else if (length(grep("ANY.COMPGRADE3.", compModelId[i])) > 0) {
    outcomeId <- "anyComp3"
  }
  else if (length(grep("WOUND.COMPGRADE2.", compModelId[i])) > 0) {
    outcomeId <- "woundInf2"
  }
  else if (length(grep("WOUND.COMPGRADE3.", compModelId[i])) > 0) {
    outcomeId <- "woundInf3"
  }
  else if (length(grep("CELLULITIS.COMPGRADE2.", compModelId[i])) > 0) {
    outcomeId <- "cellulitis2"
  }
  else if (length(grep("CELLULITIS.COMPGRADE3.", compModelId[i])) > 0) {
    outcomeId <- "cellulitis3"
  }
  else if (length(grep("SEROMA.COMPGRADE2.", compModelId[i])) > 0) {
    outcomeId <- "seroma2"
  }
  else if (length(grep("SEROMA.COMPGRADE3.", compModelId[i])) > 0) {
    outcomeId <- "seroma3"
  }  
  else if (length(grep("GRAFT.COMPGRADE2.", compModelId[i])) > 0) {
    outcomeId <- "graftComp2"
  }
  else if (length(grep("GRAFT.COMPGRADE3.", compModelId[i])) > 0) {
    outcomeId <- "graftComp3"
  }
  
  else{
    message <- 'Id ' + compModelId[i] + ' was not processed with an outcome.'
    stop(message)
  }
  

  
  userResults <- rbind_list(userResults,
                            GenerateRate(
                                         df = AllData,
                                         outcome = outcomeId, 
                                         covariates = wideExcisionCovs,
                                         modelId = compModelId[i],
                                         modelType = "Logistic",
                                         dateVar = "surgDate",
                                         userIdVar = "userId", 
                                         patientIdVar = "eventId", 
                                         weightVar = "yos",
                                         func = SelectCohort, 
                                         imputedValues = imputedValues,
                                         date = lastSurgeryDate,
                                         procId = "Mel",
                                         ptRiskGroups = riskGroups
                                         )
                            )  
}


#### Proportion SLND 
# Proportion SLND = pt's getting SLND/all patients in our data set
# Create model id
propSLNDModelId <- paste0("SLND.", dateIds)

# Loop over all model IDs to obtain the rates for each model     
for (i in 1:length(propSLNDModelId)) {
  print(propSLNDModelId[i])
  userResults <- rbind_list(userResults,
                            GenerateRate(
                              df = AllData,
                              outcome = "slnd", 
                              covariates = wideExcisionCovs,
                              modelId = propSLNDModelId[i],
                              modelType = "Logistic",
                              dateVar = "surgDate",
                              userIdVar = "userId", 
                              patientIdVar = "eventId",
                              weightVar = "yos",
                              func = SelectCohort, 
                              imputedValues = imputedValues,
                              date = lastSurgeryDate,
                              procId = "Mel",
                              ptRiskGroups = riskGroups
                              )
                            )  
  
}


#### Proportion Positive SLND 
# Proportion positive SLND = pt's with "positive" nodes on the SLND / 
# all patients who received a SLND
# Create model id
propPosSLNDModelId <- paste0("POSSLND.", dateIds)

# Loop over all model IDs to obtain the rates for each model     
for (i in 1:length(propPosSLNDModelId)) {
  print(propPosSLNDModelId[i])
  userResults <- rbind_list(userResults,
                            GenerateRate(
                              df = AllData,
                              outcome = "posSlnd", 
                              covariates = wideExcisionCovs,
                              modelId = propPosSLNDModelId[i],
                              modelType = "Logistic",
                              dateVar = "surgDate",
                              userIdVar = "userId",
                              patientIdVar = "eventId",
                              weightVar = "yos",
                              func = SelectCohort,
                              imputedValues = imputedValues,
                              date = lastSurgeryDate,
                              procId = "Mel",
                              ptRiskGroups = riskGroups
                              )
                            ) 
  
}

#### Proportion Positive SLND then LND 
# Proportion positive SLND then LND = pt's getting complete node dissection / 
# patient's who had a positive SLND

# Create model id
propPosSLNDThenLNDModelId <- paste0("CLND.", dateIds)

# Loop over all model IDs to obtain the rates for each model     
for (i in 1:length(propPosSLNDThenLNDModelId)) {
  print(propPosSLNDThenLNDModelId[i])
  userResults <- rbind_list(userResults,
                            GenerateRate(
                              df = AllData,
                              outcome = "posSlndClnd", 
                              covariates = wideExcisionCovs,
                              modelId = propPosSLNDThenLNDModelId[i],
                              modelType = "Logistic",
                              dateVar = "surgDate",
                              userIdVar = "userId",
                              patientIdVar = "eventId",
                              weightVar = "yos",
                              func = SelectCohort,
                              imputedValues = imputedValues,
                              date = lastSurgeryDate,
                              procId = "Mel",
                              ptRiskGroups = riskGroups
                              )
                            ) 
  
}

# #### Proportion Inappropriate SLND 
# # Create model id
# propInopSLNDModelId <- paste0("PROINOPSLND.", dateIds) 
# 
# # Loop over all model IDs to obtain the rates for each model     
# for (i in 1:length(propInopSLNDModelId)) {
#   print(propInopSLNDModelId[i])
#   userResults <- rbind_list(userResults,
#                             GenerateRate(
#                               df = AllData,
#                               outcome = "propPosSLNDThenLND", 
#                               covariates = wideExcisionCovs,
#                               modelId = propInopSLNDModelId[i],
#                               modelType = "Logistic",
#                               dateVar = "surgDate",
#                               userIdVar = "userId",
#                               patientIdVar = "eventId",
#                               weightVar = "yos",
#                               func = SelectCohort,
#                               imputedValues = imputedValues,
#                               date = lastSurgeryDate,
#                               procId = "Mel")) #
#   
# }

# #### Use of Skin Graft 
# # Create model id
# graftModelId <- paste0("GRAFT.", dateIds)
# 
# # Loop over all model IDs to obtain the rates for each model     
# for (i in 1:length(graftModelId)) {
#   print(graftModelId[i])
#   userResults <- rbind_list(userResults,
#                             GenerateRate(
#                               df = AllData,
#                               outcome = "graft", 
#                               covariates = wideExcisionCovs,
#                               modelId = graftModelId[i],
#                               modelType = "Logistic",
#                               dateVar = "surgDate",
#                               userIdVar = "userId",
#                               patientIdVar = "eventId",
#                               weightVar = "yos",
#                               func = SelectCohort,
#                               imputedValues = imputedValues,
#                               date = lastSurgeryDate,
#                               procId = "Mel",
#                               ptRiskGroups = riskGroups
#                               )
#                             ) 
#   
# }

# #### Use of Flaps or Adjacent Skin 
# # Create model id
# flapsModelId <- paste0("FLAPS.", dateIds)
# 
# # Loop over all model IDs to obtain the rates for each model     
# for (i in 1:length(flapsModelId)) {
#   print(flapsModelId[i])
#   
#   userResults <- rbind_list(userResults,
#                             GenerateRate(
#                               df = AllData,
#                               outcome = "flap", 
#                               covariates = wideExcisionCovs,
#                               modelId = flapsModelId[i],
#                               modelType = "Logistic",
#                               dateVar = "surgDate",
#                               userIdVar = "userId",
#                               patientIdVar = "eventId",
#                               weightVar = "yos",
#                               func = SelectCohort,
#                               imputedValues = imputedValues,
#                               date = lastSurgeryDate,
#                               procId = "Mel",
#                               ptRiskGroups = riskGroups
#                               )
#                             ) 
#   
# }



#### Surgeon Volume 
volModelId <- paste0("VOL.", dateIds)

for (i in 1:length(volModelId)) {
  print(volModelId)
  userResults <- bind_rows(userResults, 
                           GenerateUserVolume(AllData,
                                              dateVar = "surgDate",
                                              func = SelectCohort,
                                              date = lastSurgeryDate,
                                              modelId = volModelId[i]
                                              )
                           )      
}


#----------------
#  Save results
#----------------


# Exporting all model results (adjusted and unadjusted) to CSV file
write.table(userResults, 
            file = paste0(getwd(), "/Results/SurgeonRates_full.csv"),
            sep = ",", 
            row.names = F) 

# Save out
userResults_trim <- GetSurgeonRates(userResults, keepRaw = TRUE)

# Export
write.table(userResults_trim,
            file = paste0(getwd(), "/Results/SurgeonRates.csv"),
            sep = ",", 
            row.names = F) 

# Save out workspace
save.image(paste0(getwd(),"/Results/SurgeonRates.RData"))

# Write to Results folder: userResults

# Write to Results folder: "trimmed" userResults



## Notes

# proportion slnd is 100% for everyome, but that makes sense given the data
# Ariyan and Brady have a high percentage of NAs though
# > widetab(melDf, surgeon, slnd)
# surgeon slnd   n
# 1  ARIYAN    1 145
# 2  ARIYAN   NA 134
# 3   BRADY    0   1
# 4   BRADY    1 432
# 5   BRADY   NA 393
# 6    COIT    1 840
# 7    COIT   NA 130

# > byYearCheck(melDf, slnd)
# yos     mean percNa total
# 1  2003 0.988764   0.25   119
# 2  2004 1.000000   0.22   121
# 3  2005 1.000000   0.35   170
# 4  2006 1.000000   0.45   112
# 5  2007 1.000000   0.31   131
# 6  2008 1.000000   0.28   124
# 7  2009 1.000000   0.35   138
# 8  2010 1.000000   0.31   131
# 9  2011 1.000000   0.38   113
# 10 2012 1.000000   0.28   156
# 11 2013 1.000000   0.34   157
# 12 2014 1.000000   0.32   126
# 13 2015 1.000000   0.28   140
# 14 2016 1.000000   0.34   137
# 15 2017 1.000000   0.29   154
# 16 2018 1.000000   0.39    46



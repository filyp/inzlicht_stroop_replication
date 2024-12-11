########################################################################
#This script will rank order participants to screen them for the ERN
# ManyLabs project. A .csv will be created with information on participants
# to contact to come in for the in-lab portion of the study.
#
#Required Input
# fileloc - a .csv file exported from Qualtrics. Be sure 'Download all files'
#  is checked and that the radio button for 'Use numeric values' is on.
# n_select - a number of participants to select for each group
#
#
#Optional Input
# prev_output - this should point to the previous file that was saved using 
#  this script. This information is needed to determine who was already 
#  screened for inclusion in the study in an effort to avoid repeats. If
#  prev_output is not provided, all participants will be screened.
#
#Outputs
# save_output - a file path where the participants selected to be contacted
#  should be saved
#  This .csv will contain various new columns. Most importantly...
#   group - excluded, phobia, worry, or control
#   prev_call - 1, person has been invited before,
#    0, person has not been invited before (updates each run)
#   call_me - 1, person should be invited to participate (contact!)
#    0, person should not be invited to participate
#
#
#Required Libraries
# here, tidyverse
########################################################################
#load necessary libraries
library(here)
library(tidyverse)

#Set initial variables below

#set project root
here::i_am("Many Labs Replication - ERN.Rproj")

#set file name of most recent download
fileloc <- ""

#set file name of last output (leave blank if no output)
prev_output <- ""

#how many participants should be selected from each group?
n_select <- 5

#set file name of where file should be saved
#I recommend something sensible with a datestamp of the download
# (not the datestamp for when the script was run)
save_output <- ""


########################################################################



#read files
df <- tibble(read.csv(here(fileloc),
                      header = T))

# Added CF
df <- df %>% 
  mutate(across(everything(), ~ifelse(.=="Nein" | .=="Falsch", 0,.))) %>%
  mutate(across(everything(), ~ifelse(.=="Ja" | .=="Wahr", 1,.))) %>%
  mutate(across(everything(), ~ifelse(.=="überhaupt nicht typisch für mich", 1,.))) %>%
  mutate(across(everything(), ~ifelse(.=="nur wenig typisch für mich", 2,.))) %>%
  mutate(across(everything(), ~ifelse(.=="ziemlich typisch für mich", 3,.))) %>%
  mutate(across(everything(), ~ifelse(.=="sehr typisch für mich", 4,.))) %>%
  mutate(across(everything(), ~ifelse(.=="äußerst typisch für mich", 5,.)))

PSWQ_names = list("PSWQ_1", "PSWQ_2", "PSWQ_3", "PSWQ_4", "PSWQ_5", "PSWQ_6", "PSWQ_7", "PSWQ_8",
                  "PSWQ_9", "PSWQ_10", "PSWQ_11", "PSWQ_12", "PSWQ_13", "PSWQ_14", "PSWQ_15", "PSWQ_16")

SNAQ_names = list("SNAQ_1", "SNAQ_2", "SNAQ_3", "SNAQ_4", "SNAQ_5", "SNAQ_6", "SNAQ_7", "SNAQ_8", "SNAQ_9", "SNAQ_10", 
                  "SNAQ_11", "SNAQ_12", "SNAQ_13", "SNAQ_14", "SNAQ_15", "SNAQ_16", "SNAQ_17", "SNAQ_18", "SNAQ_19", "SNAQ_20", 
                  "SNAQ_21", "SNAQ_22", "SNAQ_23", "SNAQ_24", "SNAQ_25", "SNAQ_26", "SNAQ_27", "SNAQ_28", "SNAQ_29", "SNAQ_30")

SPQ_names = list("SPQ_1", "SPQ_2", "SPQ_3", "SPQ_4", "SPQ_5", "SPQ_6", "SPQ_7", "SPQ_8", "SPQ_9", "SPQ_10", "SPQ_11", 
                 "SPQ_12", "SPQ_13", "SPQ_14", "SPQ_15", "SPQ_16", "SPQ_17", "SPQ_18", "SPQ_19", "SPQ_20", "SPQ_21", 
                 "SPQ_22", "SPQ_23", "SPQ_24", "SPQ_25", "SPQ_26", "SPQ_27", "SPQ_28", "SPQ_29", "SPQ_30", "SPQ_31")

colnames(df)[1] <- "ResponseID"
colnames(df)[2] <- "Age"
colnames(df)[3] <- "Gender"
colnames(df)[4] <- "Current Sleep Disorder"
colnames(df)[5] <- "Post or Present Neurological Disorder"
colnames(df)[6] <- "Post or Present Psychiatric Disorder"
colnames(df)[7:22]  <- PSWQ_names
colnames(df)[23:52] <- SNAQ_names
colnames(df)[53:83] <- SPQ_names


#remove first two rows, which are descriptive.
#note that this is idempotent code
#df <- df %>% filter(StartDate != "Start Date")
#df <- df %>% filter(StartDate != "{\"ImportId\":\"startDate\",\"timeZone\":\"America/Denver\"}")


#convert column names to lowercase
colnames(df) <- tolower(colnames(df))


#filter rows based on missing data in columns with pswq in their names
df <- df %>%
  rowwise() %>%
  filter(all(c_across(contains("pswq")) != "")) %>%
  filter(all(c_across(contains("snaq")) != "")) %>%
  filter(all(c_across(contains("spq")) != "")) %>%
  filter(all(c_across(contains("eeg_interest.")) != ""))


#######################PSWQ#######################
#pull pswq
pswq_raw <- df %>%
  select(responseid, pswq_1:pswq_16) %>%
  mutate(across(-responseid, as.numeric))

#specify reverse coded items
# pswq_rev_code <- 
#   c("pswq_2","pswq_4","pswq_5","pswq_6",
#     "pswq_7","pswq_9","pswq_12","pswq_13",
#     "pswq_14","pswq_15","pswq_16")

pswq_rev_code <- c("pswq_1","pswq_3","pswq_8","pswq_10", "pswq_11")
  


pswq_raw <-
  pswq_raw %>%
  mutate(
    across(
      all_of(pswq_rev_code),
      ~ recode(.x, 
               "5" = 1, 
               "4" = 2, 
               "3" = 3, 
               "2" = 4, 
               "1" = 5,
               .default = .x)
    )
  )

#All data should be between 1 and 5
pswq_range <- 
  pswq_raw %>%
  rowwise() %>%
  mutate(
    pswq_within_range = all(between(c_across(starts_with("pswq")), 1, 5))
  ) %>%
  select(responseid, pswq_within_range)

#Are all variables within the appropriate range of values?
all(pswq_range$pswq_within_range)


pswq <-
  pswq_raw %>%
  rowwise() %>%
  mutate(
    pswq_total = sum(c_across(starts_with("pswq")), na.rm = TRUE) 
  ) %>% 
  ungroup() %>%
  select(responseid,pswq_total)

#put back in dataset
df <- merge(df,
            pswq[,c("responseid","pswq_total")])


#######################SNAQ#######################

#pull snaq
snaq_raw <- df %>%
  select(responseid, snaq_1:snaq_30) %>%
  mutate(across(-responseid, as.numeric))

#specify reverse coded items
# SNAQ_22 has to be recoded in German Version - Check your Version!
snaq_rev_code <- 
  c("snaq_6","snaq_12","snaq_14","snaq_16",
    "snaq_17","snaq_20","snaq_22", "snaq_25","snaq_27",
    "snaq_28")

#check how true false are coded so we can sum true responses
#raw 1 = true, 2 = false
#change to 1 = true, 0 = false for easy scoring
snaq_raw <-
  snaq_raw %>%
  mutate(
    across(
      starts_with("snaq"),
      ~ recode(.x,
               "1" = 1, 
               "0" = 0
      )
    ),
    across(
      all_of(snaq_rev_code),
      ~ recode(.x, 
               "1" = 0, 
               "0" = 1)
    )
  )

#All data should be between 1 and 5
snaq_range <- 
  snaq_raw %>%
  rowwise() %>%
  mutate(
    snaq_within_range = all(between(c_across(starts_with("snaq")), 0, 1))
  ) %>%
  select(responseid, snaq_within_range)

#Are all variables within the appropriate range of values?
all(snaq_range$snaq_within_range)

snaq <-
  snaq_raw %>%
  rowwise() %>%
  mutate(
    snaq_total = sum(c_across(starts_with("snaq")), na.rm = TRUE) 
  ) %>% 
  ungroup() %>%
  select(responseid,snaq_total)

#put back in dataset
df <- merge(df,
            snaq[,c("responseid","snaq_total")])





#######################SPQ#######################

#pull spq
spq_raw <- df %>%
  select(responseid, spq_1:spq_31) %>%
  mutate(across(-responseid, as.numeric))

#specify reverse coded items
spq_rev_code <- 
  c("spq_6","spq_12","spq_14","spq_16",
    "spq_17","spq_20","spq_25","spq_27",
    "spq_28")

#check how true false are coded so we can sum true responses
#raw 1 = true, 2 = false
#change to 1 = true, 0 = false for easy scoring
spq_raw <-
  spq_raw %>%
  mutate(
    across(
      starts_with("spq"),
      ~ recode(.x,
               "1" = 1, 
               "0" = 0
      )
    ),
    across(
      all_of(spq_rev_code),
      ~ recode(.x, 
               "1" = 0, 
               "0" = 1)
    )
  )

#All data should be between 1 and 5
spq_range <- 
  spq_raw %>%
  rowwise() %>%
  mutate(
    spq_within_range = all(between(c_across(starts_with("spq")), 0, 1))
  ) %>%
  select(responseid, spq_within_range)

#Are all variables within the appropriate range of values?
all(spq_range$spq_within_range)

spq <-
  spq_raw %>%
  rowwise() %>%
  mutate(
    spq_total = sum(c_across(starts_with("spq")), na.rm = TRUE) 
  ) %>% 
  ungroup() %>%
  select(responseid,spq_total)

#put back in dataset
df <- merge(df,
            spq[,c("responseid","spq_total")])

#make combined phobia score for ranking
df$snaq_spq_total <- df$snaq_total + df$spq_total



#rank participants based on worry and phobia scores
df_pswqranking <- df %>%
  arrange(pswq_total) %>%
  mutate(pswq_rank = row_number()) %>%
  arrange(snaq_spq_total) %>%
  mutate(snaq_spq_rank = row_number())

#"worry" group: prioritize low pswq_rank (high worry) and high snaq_spq_rank (low fear)
#notice I decrease weight of snaq_spq in combined_rank
worry_candidates <- df_pswqranking %>%
  mutate(combined_rank = pswq_rank - (snaq_spq_rank/3)) %>%
  arrange(desc(combined_rank)) %>%
  slice(1:n_select) %>%
  pull(responseid)

df_phobiaranking <- df_pswqranking %>%
  filter(!(responseid %in% worry_candidates)) 

#"phobia" group: prioritize low snaq_spq_rank and high pswq_rank
#notice I decrease weight of pswq_rank in combined_rank
phobia_candidates <- df_phobiaranking %>%
  filter(!(responseid %in% worry_candidates)) %>%
  mutate(combined_rank = snaq_spq_rank - (pswq_rank)/3) %>%
  arrange(desc(combined_rank)) %>%
  slice(1:n_select) %>%
  pull(responseid)

#label worry and phobia groups
df <- df %>%
  mutate(
    group = case_when(
      responseid %in% worry_candidates ~ "worry",
      responseid %in% phobia_candidates ~ "phobia",
      TRUE ~ NA_character_  
    )
  )

df_controlranking <- df %>%
  filter(is.na(group)) %>%
  arrange(pswq_total) %>%
  mutate(pswq_rank = row_number()) %>%
  arrange(snaq_spq_total) %>%
  mutate(snaq_spq_rank = row_number())


#"control" prioritize low combined ranks of both pswq and snaq_spq
control_candidates <- df_controlranking %>%
  mutate(combined_rank = pswq_rank + snaq_spq_rank) %>%
  arrange(combined_rank) %>%
  slice(1:n_select) %>%
  pull(responseid)  

#label control and excluded groups
df <- df %>%
  mutate(
    group = case_when(
      responseid %in% control_candidates ~ "control",
      is.na(group) ~ "excluded",
      TRUE ~ as.character(group)
    )
  )


print("summary stats for current pull:")

#pull descriptives
desc_stats_pswq <- df %>%
  filter(group != "excluded") %>% 
  group_by(group) %>%
  summarize(
    count = n(),
    pswq_mean = mean(pswq_total, na.rm = TRUE),
    pswq_median = median(pswq_total, na.rm = TRUE),
    pswq_range = paste0(min(pswq_total, na.rm = TRUE), "-", max(pswq_total, na.rm = TRUE)),
  )

desc_stats_snaq <- df %>%
  filter(group != "excluded") %>% 
  group_by(group) %>%
  summarize(
    count = n(),
    snaq_spq_mean = mean(snaq_spq_total, na.rm = TRUE),
    snaq_spq_median = median(snaq_spq_total, na.rm = TRUE),
    snaq_spq_range = paste0(min(snaq_spq_total, na.rm = TRUE), "-", max(snaq_spq_total, na.rm = TRUE))
  )


#view results
print(desc_stats_pswq) #worry group should have highest score
print(desc_stats_snaq) #phobia group should have highest score


#if there was a previous output already provided, load it to compare
if (prev_output != "") {
  #read previous file
  df_prev <- tibble(read.csv(here(prev_output),
                             header = T))
  
  #for the first time this script is used (prev_call won't exist yet)
  if (!"prev_call" %in% names(df_prev)) {
    df_prev$prev_call <- 0
  }
  
  #identify participants that were already selected to be invited  
  df_prev <- df_prev %>%
    mutate(
      prev_call = 
        case_when(
          prev_call == 1 ~ 1,
          call_me == 1 ~ 1,
          TRUE ~ 0
        )
    )
  
  #combine the dataframes and identify people to follow up with
  df <- df %>%
    left_join(df_prev %>% select(responseid, prev_call), by = "responseid") %>%
    mutate(prev_call = if_else(is.na(prev_call), 0, prev_call)) %>%
    mutate(
      call_me = case_when(
        prev_call == 1 ~ 0,
        prev_call == 0 & group != "excluded" ~ 1,
        TRUE ~ 0   
      )
    )
  
} else {
  #for when there is no previous file to consider, call everyone
  df <- df %>%
    mutate(
      call_me = case_when(
        group != "excluded" ~ 1,
        TRUE ~ 0 
      )
    )
}

df %>% 
  filter(call_me == 1) %>% 
  select(responseid, `current sleep disorder`, `post or present neurological disorder`, 
         `post or present psychiatric disorder`,  group, pswq_total, snaq_spq_total)

#save output
write.csv(df,
          file = here(save_output),
          row.names = F)


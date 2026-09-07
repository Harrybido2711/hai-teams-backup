#!/usr/bin/env bash
#SBATCH --account=p32983
#SBATCH --partition=long
#SBATCH --array=0-4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4GB
#SBATCH --time=16:00:00
#SBATCH --job-name=gemini35lite_mmlu_google
#SBATCH --output=log_shard%a.txt
#SBATCH --error=log_shard%a.err

# 5 shards, the project's measured ceiling (quest-cluster.md), and here it is also NOT a free
# choice: this run resumes a 5-shard checkpoint copied from MMLU_Gemini_Flash3.5lite_OpenRouter.
# Each array task reads back its own <model>_shard<N>of5.jsonl, keeps the rows that have a response
# and re-asks the ones that came back empty when OpenRouter's balance ran out. Change --total-shards
# and every shard reads the wrong checkpoint.
#
# Only the ~2,188 empty rows are re-asked; the 1,755 rows that OpenRouter answered are kept, so this
# result set is deliberately two routes and every row's `config` column says which one wrote it.
#
# Submit from inside this folder. When all five finish, merge:
#   python ../merge_mmlu_shards.py --model google/gemini-3.5-flash-lite --model-dir . --total-shards 5
# The merge refuses to stay quiet about a missing shard: it reports which, merges what exists, and
# exits 1 so a partial number is never mistaken for a whole one.

module purge
export PYTHONUNBUFFERED=1

/projects/p32983/pythonenvs/hai-teams/bin/python gemini35lite_mmlu_eval.py \
    --model google/gemini-3.5-flash-lite \
    --subject all \
    --prompt v2 \
    --shard "$SLURM_ARRAY_TASK_ID" \
    --total-shards 5

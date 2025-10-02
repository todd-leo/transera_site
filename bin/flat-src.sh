#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
OUT="${2:-all_sources.txt}"

# 可选：开启扩展名白名单（1 开启，0 关闭）
ENABLE_EXT_FILTER=1
INCLUDE_EXTS="
py html htm js mjs cjs ts tsx
css scss sass
json yml yaml
md markdown rst txt
svg xml
ini toml cfg conf
graphql gql jinja jinja2 po
"

# 依赖与 .gitignore 检查
if ! command -v git >/dev/null 2>&1; then
  echo "Error: git not found. Please install Git." >&2
  exit 1
fi

ROOT_ABS="$(cd "$ROOT" && pwd)"
if [ ! -f "$ROOT_ABS/.gitignore" ]; then
  echo "Error: .gitignore not found under $ROOT_ABS." >&2
  exit 1
fi

# 解析输出路径为绝对路径
# 1) 如果 OUT 含目录部分，按其目录解析；否则为当前工作目录下的文件
OUT_DIR_PART="$(dirname "$OUT")"
if [ "$OUT_DIR_PART" = "." ]; then
  OUT_DIR_ABS="$PWD"
else
  # 若是相对路径，转为绝对路径；若不存在则尝试创建
  if [ -d "$OUT_DIR_PART" ]; then
    OUT_DIR_ABS="$(cd "$OUT_DIR_PART" && pwd)"
  else
    # 尝试创建目录
    mkdir -p "$OUT_DIR_PART"
    OUT_DIR_ABS="$(cd "$OUT_DIR_PART" && pwd)"
  fi
fi
OUT_BASENAME="$(basename "$OUT")"
OUT_ABS="$OUT_DIR_ABS/$OUT_BASENAME"

# 选择一个可写的临时目录：优先用输出目录，否则退回系统临时目录
TMP_DIR="$OUT_DIR_ABS"
if [ ! -w "$TMP_DIR" ]; then
  TMP_DIR="${TMPDIR:-/tmp}"
fi

# 在可写目录创建临时文件（避免覆盖已有文件）
# 注意：mktemp 在 macOS 上使用模板末尾的 XXXXXX
TMP_OUT="$(mktemp "$TMP_DIR/${OUT_BASENAME}.tmp.XXXXXX")"

# 写入头部到临时文件
{
  echo "# ===== Concatenated Sources ====="
  echo "# Root: ${ROOT_ABS}"
  echo "# Encoding: UTF-8"
  echo
} > "$TMP_OUT"

# 扩展名匹配函数
matches_ext() {
  # $1: relative path
  if [ "$ENABLE_EXT_FILTER" -ne 1 ]; then
    return 0
  fi
  local p="$1"
  local ext
  for ext in $INCLUDE_EXTS; do
    case "$p" in
      *."$ext") return 0 ;;
    esac
  done
  return 1
}

# 统计
files_count=0
lines_count=0

# 列出候选文件（绝对路径）并排序
files_list="$(
  find "$ROOT_ABS" -type f -print \
    | LC_ALL=C sort
)"

# 逐个处理
printf '%s\n' "$files_list" | while IFS= read -r src_abs; do
  [ -z "$src_abs" ] && continue

  # 排除输出文件（目标与临时）
  if [ "$src_abs" = "$OUT_ABS" ] || [ "$src_abs" = "$TMP_OUT" ]; then
    continue
  fi

  # 相对路径
  rp="${src_abs#$ROOT_ABS/}"
  case "$rp" in
    /*) continue ;;
  esac

  # .gitignore 过滤
  if git -C "$ROOT_ABS" check-ignore --quiet -- "$rp"; then
    continue
  fi

  # 扩展名白名单（可选）
  if ! matches_ext "$rp"; then
    continue
  fi

  # 进度输出：开始处理
  printf 'Processing: %s\n' "$rp"

  # 写入内容
  {
    echo "# ----- BEGIN FILE: ${rp} -----"
    if ! cat "$src_abs" 2>/dev/null; then
      echo "# [SKIPPED: unreadable]"
    fi

    # 确保结尾换行
    if [ -s "$src_abs" ]; then
      if tail -c1 "$src_abs" 2>/dev/null | od -An -t x1 2>/dev/null | grep -qi '0a'; then
        :
      else
        echo
      fi
    else
      echo
    fi

    echo "# ----- END FILE: ${rp} -----"
    echo
  } >> "$TMP_OUT"

  # 累积统计
  files_count=$((files_count + 1))
  f_lines=$(LC_ALL=C wc -l < "$src_abs" 2>/dev/null || echo 0)
  lines_count=$((lines_count + f_lines))

  # 进度输出：完成该文件后的累计统计
  printf 'Done: files=%d, lines=%d\n' "$files_count" "$lines_count"
done

# 将统计从子 shell 回传
stats_tmp="$(mktemp "${TMP_DIR}/stats.XXXXXX")"
printf "%s %s\n" "${files_count:-0}" "${lines_count:-0}" > "$stats_tmp"
read files_total lines_total < "$stats_tmp"
rm -f "$stats_tmp"

# 附加统计
{
  echo "# ===== Statistics ====="
  echo "# Files: ${files_total:-0}"
  echo "# Lines: ${lines_total:-0}"
} >> "$TMP_OUT"

# 原子覆盖目标（若目标目录不可写将失败并报错）
mv -f "$TMP_OUT" "$OUT_ABS"

echo "Written: $OUT_ABS"
echo "Files processed: ${files_total:-0}"
echo "Total lines: ${lines_total:-0}"
#!/usr/bin/env python3
"""
Decode base64 subscription content and validate node links
"""
import base64
import re
import sys
from pathlib import Path


def decode_and_validate(input_file: str) -> None:
    """
    Decode base64 content if needed and validate node links
    
    Args:
        input_file: Path to input file containing subscription data
        
    Raises:
        SystemExit: If file is invalid or cannot be decoded
    """
    p = Path(input_file)
    
    # Read file content
    raw = p.read_text(encoding="utf-8", errors="ignore").strip()
    if not raw:
        raise SystemExit(f"{input_file} 为空")
    
    # Try to decode as base64
    payload = "".join(raw.split())
    
    # Check if it looks like base64
    if not re.fullmatch(r"[A-Za-z0-9+/=]+", payload):
        raise SystemExit("不是 base64 内容，也没有找到支持的节点链接")
    
    # Attempt base64 decoding
    try:
        decoded = base64.b64decode(payload, validate=True).decode("utf-8", errors="ignore")
    except Exception as exc:
        raise SystemExit(f"Base64 解码失败: {exc}")
    
    # Validate decoded content
    if not re.search(r"(vmess|vless|ss|trojan|hysteria2)://", decoded):
        raise SystemExit("Base64 解码后未发现支持的节点链接")
    
    # Write decoded content back
    p.write_text(decoded, encoding="utf-8")
    print("Base64 解码成功")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python decode_base64.py <input_file>")
        sys.exit(1)
    
    decode_and_validate(sys.argv[1])

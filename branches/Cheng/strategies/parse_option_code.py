def parse_option_code(option_code):
  
    code  = option_code.split('.')[0]
    if '-' in code:
        parts = code.split('-')
        if len(parts) == 3:
            underlying = parts[0]
            option_type = 'call' if parts[1].upper() == 'C' else 'put'
            strike = int(parts[2])
        else:
            import traceback
            traceback.print_exc()

    else:

        call_pos = code.find('C') # 找不到指定字符串的时候返回 -1
        put_pos = code.find('P')

        if call_pos != -1:
            option_type = 'call'
            underlying = code[:call_pos]
            strike = int(code[call_pos + 1:])
        elif put_pos != -1:
            option_type = 'put'
            underlying = code[:put_pos]
            strike = int(code[put_pos + 1:])
        else:
            import traceback
            traceback.print_exc()

    return {
        'option_type': option_type,
        'underlying': underlying,
        'strike': strike,
        'exchange': option_code.split('.')[-1] if '.' in option_code else None
    }
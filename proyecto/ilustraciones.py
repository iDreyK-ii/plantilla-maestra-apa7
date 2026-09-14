"""Iconos vectoriales propios, incorporados al HTML y sin recursos externos."""
def study_icon(kind):
    shapes={
        'book':'<path d="M5 8q6-3 11 0 5-3 11 0v18q-5-3-11 0-5-3-11 0Z" fill="#fffdfb"/><path d="M16 8v18M8 12h4M20 12h4"/><circle cx="11" cy="18" r=".8"/><circle cx="21" cy="18" r=".8"/><path d="M14 20q2 2 4 0"/>',
        'pencil':'<path d="m8 21 13-15q2-2 5 1t1 5L13 27l-7 2Z" fill="#f8dce5"/><path d="m8 21 5 6M19 9l6 6M6 29l3-1"/><path d="m12 21 9-10"/>',
        'document':'<path d="M9 4h11l6 6v19H6V7q0-3 3-3Z" fill="#fffdfb"/><path d="M20 4v7h6M11 16h10M11 21h7"/><path d="m11 25 2 1 3-3"/>',
        'search':'<circle cx="14" cy="14" r="9" fill="#fffdfb"/><path d="m21 21 7 7M10 12h8M10 16h5"/>',
        'heart':'<path d="M16 26C-2 15 5 1 16 10 27 1 34 15 16 26Z" fill="#f8dce5"/><path d="m10 17 4-4 3 6 3-4h3"/>'
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+shapes[kind]+'</svg>'

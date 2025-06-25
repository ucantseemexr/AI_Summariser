from split_table import detect_table_boundaries_by_cluster_change
def build_JSON_prompt(rows):
    markdown_table = parse_table_to_markdown(rows)
    
    print(markdown_table)
    prompt = f"""
Task: Convert structured tables to clean, properly nested JSON format.

You are a precise and intelligent JSON converter for structured tables. Given a markdown table, output a valid JSON array where:

- Each logical row corresponds to a JSON object.
- The first non-empty cell in a row is treated as the primary identifier (e.g., entity name), and used as a key called "Label" unless a header specifies otherwise.
- Column headers define the keys for the JSON fields.
- If a row beneath an entity contains sub-fields (e.g., Part1, RegionA), nest those under the appropriate parent key (e.g., "Population", "Sales").
- If headers are missing or reused from prior rows, assume they are inherited from above.
- All values must be output as strings.
- Do not include any explanation or commentary — only output the resulting JSON.

{examples}
----------------

Now convert the following table:

Table:
{markdown_table}

JSON:
    """
    
    return prompt

def parse_table_to_markdown(rows):
    markdown_lines = []
    boundaries = detect_table_boundaries_by_cluster_change(rows)
    
    for i in range(len(rows)):
      if i in boundaries:
        markdown_lines.append("\n=== New Table ===\n")
      line = '|' + '|'.join(cell.strip() for cell in rows[i]) + '|'
      markdown_lines.append(line)
        
    return '\n'.join(markdown_lines)


examples =f"""
Table:
|Empty Cell|  Population    |    GDP      |
| China   |   1.3 bil      |    10bil    |
|Empty Cell| Pop1   | Pop2  | GDP1 | GDP2 |
| US      | 500mil | 20mil | 6bil | 4bil |

JSON:
[
  {{
    "Label": "China",
    "Population": "1.3 bil",
    "GDP": "10bil"
  }},
  {{
    "Label": "US",
    "Population": {{
      "Pop1": "500mil",
      "Pop2": "20mil"
    }},
    "GDP": {{
      "GDP1": "6bil",
      "GDP2": "4bil"
    }}
  }}
]
=== End of Ouput ===

Table:
|Empty Cell| Population      |Empty Cell| GDP  |
| France   | Urban | Rural   |Empty Cell| 3bil |
|Empty Cell| 40mil | 20mil   |Empty Cell|Empty Cell|

JSON:
[
  {{
    "Label": "France",
    "Population": {{
      "Urban": "40mil",
      "Rural": "20mil"
    }},
    "GDP": "3bil"
  }}
]
=== End of Output ===

Table:
|Empty Cell|         Population          |   GDP    |
|Empty Cell| Region1 | Region2 | Region3 |Empty Cell|
|  Brazil  | 70mil    | 80mil   | 62mil  |  1.8bil  |

JSON:
[
  {{
    "Label": "Brazil",
    "Population": {{
      "Region1": "70mil",
      "Region2": "80mil",
      "Region3": "62mil"
    }},
    "GDP": "1.8bil"
  }}
]
=== End of Output ==

Table:
|Empty Cell|  Population    |    GDP      |
| China    |   1.3 bil      |    10bil    |
| US       |     500mil     |Empty Cell   |

JSON:
[
  {{
    "Label": "China",
    "Population": "1.3 bil",
    "GDP": "10bil"
  }},
  {{
    "Label": "US",
    "Population": "500mil",
    "GDP": "Missing"
  }}
]
=== End of Ouput ===

Table:
|Empty Cell| Price |Empty Cell|Empty Cell|
| Product  | USD   |   EUR    |   SGD    |
| Apple    | 1.2   |   1.0    |   1.6    |

JSON:
[
  {{
    "Label": "Apple",
    "Price": {{
      "USD": "1.2",
      "EUR": "1.0",
      "SGD": "1.6"
    }}
  }}
]
=== End of Output ===

Table:
| Department | Q1 Revenue | Q2 Revenue |
| Sales      | $1.2M      | $1.5M      |
| Marketing  | $900K      | $1.1M      |
| HR         | $500K      | $600K      |

=== New Table ===

| Product   | Units Sold | Return Rate |
| Widget A  | 12,000     | 2.5%        |
| Widget B  | 8,000      | 1.9%        |
| Widget C  | 5,000      | 3.0%        |

=== New Table ===

| Project | Deadline     | Owner   |
| Alpha   | 2024-09-30   | Liam    |
| Beta    | 2024-10-15   | Olivia  |
| Gamma   | 2024-12-01   | Ethan   |

JSON:
[
  {{
    "Label": "Sales",
    "Q1 Revenue": "$1.2M",
    "Q2 Revenue": "$1.5M"
  }},
  {{
    "Label": "Marketing",
    "Q1 Revenue": "$900K",
    "Q2 Revenue": "$1.1M"
  }},
  {{
    "Label": "HR",
    "Q1 Revenue": "$500K",
    "Q2 Revenue": "$600K"
  }}
]
[
  {{
    "Label": "Widget A",
    "Units Sold": "12,000",
    "Return Rate": "2.5%"
  }},
  {{
    "Label": "Widget B",
    "Units Sold": "8,000",
    "Return Rate": "1.9%"
  }},
  {{
    "Label": "Widget C",
    "Units Sold": "5,000",
    "Return Rate": "3.0%"
  }}
]
[
  {{
    "Label": "Alpha",
    "Deadline": "2024-09-30",
    "Owner": "Liam"
  }},
  {{
    "Label": "Beta",
    "Deadline": "2024-10-15",
    "Owner": "Olivia"
  }},
  {{
    "Label": "Gamma",
    "Deadline": "2024-12-01",
    "Owner": "Ethan"
  }}
]
=== End of Output ===
"""
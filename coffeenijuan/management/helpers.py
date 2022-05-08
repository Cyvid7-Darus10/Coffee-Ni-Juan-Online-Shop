import io
import xlsxwriter
from django.http import FileResponse

def excelreport(request, items, item_type):

  buffer = io.BytesIO()
  workbook = xlsxwriter.Workbook(buffer)
  worksheet = workbook.add_worksheet()

  # Start from the first cell. Rows and columns are zero indexed.
  row = 0
  col = 0

  # Check the item type
  if item_type == "inventory" or item_type == "supply":
    # Add the header with bold format
    header_format = workbook.add_format({
      'bold': True,
      'align': 'center',
      'valign': 'vcenter',
      'fg_color': '#D7E4BC',
      'border': 1,
      'text_wrap': True
    })
    if item_type == "supply":
      worksheet.write(row, col, "Supply Name", header_format)
    else:
      worksheet.write(row, col, "Product Name", header_format)
    worksheet.write(row, col + 1, "Price", header_format)
    worksheet.write(row, col + 2, "Stock", header_format)

    if item_type == "inventory":
      worksheet.write(row, col + 3, "Rating", header_format)

    # Set the column's width to header size
    worksheet.set_column(col, col + 3, 20)

    # wrap the text in the cell
    wrap_format = workbook.add_format({
      'text_wrap': True,
      'valign': 'vcenter',
      'border': 1
    })

    # Iterate through the items
    for item in items:
      row += 1
      worksheet.write(row, col, item.label, wrap_format)
      worksheet.write(row, col + 1, item.price, wrap_format)
      worksheet.write(row, col + 2, item.stock, wrap_format)
      if item_type == "inventory":
        worksheet.write(row, col + 3, item.rating, wrap_format)

  # Close the workbook
  workbook.close()

  # FileResponse sets the Content-Disposition header so that browsers
  # present the option to save the file.
  buffer.seek(0)
  return FileResponse(buffer, as_attachment=True, filename='{}.xlsx'.format(item_type))
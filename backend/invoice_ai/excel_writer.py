import os
import pandas as pd

OUTPUT_FOLDER = "output"
EXCEL_FILE = os.path.join(OUTPUT_FOLDER, "invoice_data.xlsx")


SUMMARY_COLUMNS = [
    "Source File",
    "Invoice Number",
    "Invoice Date",
    "Order Number",
    "Order Date",

    "Vendor Name",
    "Vendor Address",
    "Vendor GST Number",
    "Vendor PAN Number",

    "Buyer Name",
    "Buyer Address",
    "Buyer GST Number",

    "Billing Address",
    "Shipping Address",

    "Place of Supply",
    "Place of Delivery",

    "Payment Method",
    "Currency",

    "Subtotal",
    "CGST",
    "SGST",
    "IGST",
    "Tax",
    "Shipping Charges",
    "Discount",
    "Grand Total",
    "Amount In Words",

    "Item Count"
]


ITEM_COLUMNS = [
    "Invoice Number",
    "Item Name",
    "HSN/SAC",
    "Quantity",
    "Unit Price",
    "Discount",
    "Tax %",
    "Tax Amount",
    "Total Amount"
]


def save_invoice(data):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # ---------------- Summary ---------------- #

    summary_row = {}

    for col in SUMMARY_COLUMNS:
        summary_row[col] = data.get(col, "")

    # ---------------- Items ---------------- #

    item_rows = []

    items = data.get("Items", [])

    if isinstance(items, list):

        for item in items:

            row = {
                "Invoice Number": data.get("Invoice Number", "")
            }

            for col in ITEM_COLUMNS:

                if col == "Invoice Number":
                    continue

                row[col] = item.get(col, "")

            item_rows.append(row)

    # ---------------- Existing Excel ---------------- #

    if os.path.exists(EXCEL_FILE):

        try:

            summary_df = pd.read_excel(
                EXCEL_FILE,
                sheet_name="Invoice Summary"
            )

        except:

            summary_df = pd.DataFrame(columns=SUMMARY_COLUMNS)

        try:

            items_df = pd.read_excel(
                EXCEL_FILE,
                sheet_name="Invoice Items"
            )

        except:

            items_df = pd.DataFrame(columns=ITEM_COLUMNS)

    else:

        summary_df = pd.DataFrame(columns=SUMMARY_COLUMNS)
        items_df = pd.DataFrame(columns=ITEM_COLUMNS)

    # ---------------- Append ---------------- #

    summary_df = pd.concat(
        [summary_df, pd.DataFrame([summary_row])],
        ignore_index=True
    )

    if item_rows:

        items_df = pd.concat(
            [items_df, pd.DataFrame(item_rows)],
            ignore_index=True
        )

    # ---------------- Save ---------------- #

    try:

        with pd.ExcelWriter(
            EXCEL_FILE,
            engine="openpyxl"
        ) as writer:

            summary_df.to_excel(
                writer,
                sheet_name="Invoice Summary",
                index=False
            )

            items_df.to_excel(
                writer,
                sheet_name="Invoice Items",
                index=False
            )

        print(f"\n✓ Excel Updated Successfully\n{EXCEL_FILE}")

    except PermissionError:

        print(
            "\nERROR: invoice_data.xlsx is currently open.\n"
            "Please close the Excel file and upload again."
        )
import json
import logging

def read_names_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            names = set()
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    names.add((parts[0], parts[-1]))
                elif parts:
                    logging.warning(f"Skipping invalid name format in line: {line.strip()}")
            return names
    except FileNotFoundError:
        logging.error(f"File {file_path} not found!")
        return set()
    except Exception as e:
        logging.error(f"Error reading names from file {file_path}: {e}")
        return set()

def save_results(emails, file_format):
    filename = f"results.{file_format}"
    emails = [email.lower() for email in emails]
    try:
        if file_format == "txt":
            with open(filename, "w") as f:
                f.write("\n".join(emails))
        elif file_format == "json":
            with open(filename, "w") as f:
                json.dump(list(emails), f, indent=4)
        elif file_format == "csv":
            with open(filename, "w") as f:
                f.write("email\n" + "\n".join(emails))
        else:
            logging.error(f"Unsupported file format: {file_format}")
            return
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving results to {filename}: {e}")

import json
import tempfile
import yaml
import App.FFLib.AINB.ainb as ainb
import sys
import os


def ainb_to_json(input_, mode="d"): # Converts input AINB file to JSON
    data = None
    match mode:
        case "fp":
            with open(input_, 'rb') as f_in:
                data = f_in.read()
        case "d":
            data = input_
    file = ainb.AINB(data)
    temp_dir = tempfile.TemporaryDirectory()
    with open(os.path.join(temp_dir.name, "file.json"), 'w', encoding='utf-8') as outfile:
        json.dump(file.output_dict, outfile, ensure_ascii=False, indent=4)
    with open(os.path.join(temp_dir.name, "file.json"), 'r', encoding='utf-8') as f_in:
        output = f_in.read()
    temp_dir.cleanup()
    return output


def json_to_ainb(input_, mode='d', out_path=None):  # Converts input JSON file to AINB

    match mode:

        case "fout":

            with open(input_, 'r', encoding='utf-8') as f_in:
                data = json.load(f_in)

            file = ainb.AINB(data, from_dict=True)

            with open(out_path + file.filename + ".ainb", 'wb') as outfile:
                file.ToBytes(file, outfile)

        case "fp":

            with open(input_, 'r', encoding='utf-8') as f_in:
                data = json.load(f_in)

            file = ainb.AINB(data, from_dict=True)
            temp_dir = tempfile.TemporaryDirectory()

            with open(temp_dir.name + "file.ainb", 'wb') as outfile:
                file.ToBytes(file, outfile)

            with open(temp_dir.name + "file.ainb", 'rb') as f_in:
                output = f_in.read()

            temp_dir.cleanup()
            return output

        case "d":

            temp_dir = tempfile.TemporaryDirectory()

            with open(temp_dir.name + "file.json", "w", encoding="utf-8") as f_out:
                f_out.write(input_)

            with open(temp_dir.name + "file.json", "rb") as f_in:
                data = json.load(f_in)

            temp_dir.cleanup()

            file = ainb.AINB(data, from_dict=True)

            with open(temp_dir.name + "file.ainb", 'wb') as outfile:
                file.ToBytes(file, outfile)

            with open(temp_dir.name + "file.ainb", 'rb') as f_in:
                output = f_in.read()

            temp_dir.cleanup()
            return output


def ainb_to_yaml(input_, mode='d'):  # Converts input AINB file to YAML

    match mode:

        case 'd':

            file = ainb.AINB(input_)

            temp_dir = tempfile.TemporaryDirectory()

            with open(temp_dir.name + "file.yml", 'w', encoding='utf-8') as outfile:
                yaml.dump(file.output_dict, outfile, sort_keys=False, allow_unicode=True, encoding='utf-8')

            with open(temp_dir.name + "file.yml", 'r', encoding='utf-8') as f_in:
                output = f_in.read()

            temp_dir.cleanup()

            return output


def yaml_to_ainb(input_, mode='d'):  # Converts input YAML file to AINB

    match mode:

        case 'fp':

            with open(input_, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            file = ainb.AINB(data, from_dict=True)

            temp_dir = tempfile.TemporaryDirectory()

            with open(temp_dir.name + "outfile.ainb", 'wb') as outfile:
                file.ToBytes(file, outfile)

            with open(temp_dir.name + "outfile.ainb", 'rb') as f_in:
                output = f_in.read()

            temp_dir.cleanup()
            return output

        case 'd':

            temp_dir = tempfile.TemporaryDirectory()

            with open(temp_dir.name + 'file.yaml') as f_out:
                f_out.write(input_)

            with open(temp_dir.name + 'file.yaml', 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            file = ainb.AINB(data, from_dict=True)

            with open(temp_dir.name + "outfile.ainb", 'wb') as outfile:
                file.ToBytes(file, outfile)

            with open(temp_dir.name + "outfile.ainb", 'rb') as f_in:
                output = f_in.read()

            temp_dir.cleanup()
            return output


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[2]):
            if sys.argv[1] in ["ainb_to_json", "ainb_to_yaml"]:
                files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".ainb"]
            elif sys.argv[1] == "json_to_ainb":
                files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".json"]
            elif sys.argv[1] == "yaml_to_ainb":
                files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] in [".yml", ".yaml"]]
            for file in files:
                globals()[sys.argv[1]](os.path.join(sys.argv[2], file))
        else:
            globals()[sys.argv[1]](sys.argv[2])
    else:
        sys.argv.append(input("Input command name: "))
        if sys.argv[1].lower() in ["h", "help"]:
            print("Valid Commands: ainb_to_json, json_to_ainb, ainb_to_yaml, yaml_to_ainb")
            sys.argv[1] = input("Input command name: ")
        elif sys.argv[1] not in ["ainb_to_json", "json_to_ainb", "ainb_to_yaml", "yaml_to_ainb"]:
            raise ValueError("Invalid Command")
        if len(sys.argv) > 2:
            if os.path.isdir(sys.argv[2]):
                if sys.argv[1] in ["ainb_to_json", "ainb_to_yaml"]:
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".ainb"]
                elif sys.argv[1] == "json_to_ainb":
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".json"]
                elif sys.argv[1] == "yaml_to_ainb":
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] in [".yml", ".yaml"]]
                for file in files:
                    globals()[sys.argv[1]](os.path.join(sys.argv[2], file))
            else:
                globals()[sys.argv[1]](sys.argv[2])
        else:
            sys.argv.append(input("Input filepath: "))
            if os.path.isdir(sys.argv[2]):
                if sys.argv[1] in ["ainb_to_json", "ainb_to_yaml"]:
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".ainb"]
                elif sys.argv[1] == "json_to_ainb":
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] == ".json"]
                elif sys.argv[1] == "yaml_to_ainb":
                    files = [i for i in os.listdir(sys.argv[2]) if os.path.splitext(i)[1] in [".yml", ".yaml"]]
                for file in files:
                    globals()[sys.argv[1]](os.path.join(sys.argv[2], file))
            else:
                globals()[sys.argv[1]](sys.argv[2])
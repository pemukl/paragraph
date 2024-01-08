// write a typescript class that represents the structure of the above JSON
// and write a function that takes the above JSON and returns an instance of the class

export class Link {
  url!: string;
  start_idx!: string;
  stop_idx!: string;
}

export function linkFromJson(json: {
  type: string;
  start_idx: string;
  stop_idx: string;
  url: string;
}): Link {
  const reference = new Link();
  reference.start_idx = json.start_idx;
  reference.stop_idx = json.stop_idx;
  reference.url = json.url;
  return reference;
}

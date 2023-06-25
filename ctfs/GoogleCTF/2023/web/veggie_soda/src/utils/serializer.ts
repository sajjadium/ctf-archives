// @ts-ignore  
import { Serializer } from "https://deno.land/x/superserial/mod.ts";

import models from "../models/index.ts";

const serializer = new Serializer({ classes: models.opts });

export default serializer;
import {e, r} from '../../../slim-container';
import {warn} from '@pyanalyzer/logging';
import {buildpyanalyzerName, pyanalyzerNameAnonymous} from '@pyanalyzer/naming';

export default (sym_data: string, ref_data: string, g: string, c: string) => {
  const sym_raw = JSON.parse(sym_data);
  const ref_raw = JSON.parse(ref_data);

  // Manually add relation ids
  let entId = 1;
  let relationId = 0;


  let sym_dic = {};

  for (const ent of sym_raw) {
    const extra = {} as any;
    let type = ent['kind'] as string;

    // Module
    if (/MODULE/.test(type)) {
      type = 'module';
    }
    // Variable
    else if (/SCOPE/.test(type)) {
      type = 'variable';
    }
    else if (/VARIABLE/.test(type)) {
      type = 'variable';
    }
    else if (/FUNCTION/.test(type)) {
      type = 'function';
    }
    // Parameter
    else if (/PARAMETER/.test(type)) {
      type = 'parameter';
    }
    // Class
    else if ('CLASS' === type) {
      type = 'class';
    }
    else if (/ATTRIBUTE/.test(type)) {
      type = 'attribute';
    }
    else if (/CONSTRUCTOR/.test(type)) {
      type = 'function';
    }
    else if (/METHOD/.test(type)) {
      type = 'function';
    }
    // AnonymousFunction
    // Unmatched
    else {
      warn(`Unmapped type pyanalyzer/python/entity/${type}`);
      continue;
    }
    let path = ent['path'];
    path = path.replace(`../Data/RQ1/results/cases/_${g}/_${c}/`, '');
    const nameSegment = path.split('/');
    let fullname = '';
    if (nameSegment.length === 1) {
      fullname = nameSegment[0];
    } else {
      for (let i = 0; i < nameSegment.length; i++) {
        if (i !== 0) {
          fullname += '.';
        }
        fullname += nameSegment[i];
      }
    }

    let name: any = nameSegment.at(-1);
    const testAnonymity = /\(\d+\)/.exec(name!);
    if (testAnonymity) {
      name = buildpyanalyzerName<pyanalyzerNameAnonymous>({as: 'Function'});
    } else {
      name = buildpyanalyzerName(name);
    }

    e.add({
      id: entId,
      type: type,
      name: name,
      fullname,
      sourceFile: undefined,
      location: {
        start: {
          line: undefined,
          column: undefined,
        },
        end: {
          line: undefined,
          column: undefined,
        },
      },
      ...extra,
    });


    // @ts-ignore
    sym_dic[ent['path']] = entId;
    entId++;
  }

  console.log('------------------------------');
  for (const rel of ref_raw) {
    const extra = {} as any;
    // @ts-ignore
    let toId = sym_dic[rel['sym']];

    const from = undefined;
    const to = e.getById(toId);
    const type = undefined;

    r.add({
      id: relationId++,
      from,
      to,
      type,
      location: {
        file: undefined,
        start: {
          line: undefined,
          column: undefined,
        },
      },
      ...extra,
    });
  }
};

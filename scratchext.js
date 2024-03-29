class TestExt {
  getInfo() {
    return {
      id: 'testext', // change this if you make an actual extension!
      name: 'test',
      blocks: [
        {
          opcode: 'test',
          blockType: Scratch.BlockType.BOOLEAN,
          text: 'hi [ONE] [TWO]',
          arguments: {
            ONE: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'a'
            },
            TWO: {
              type: Scratch.ArgumentType.STRING,
              defaultValue: 'b'
            }
          }
        }
      ]
    };
  }
  test(args) {
    // Note strict equality: Inputs must match exactly: in type, case, etc.
    alert(args.ONE + args.TWO)
    return args.ONE === args.TWO;
  }
}
Scratch.extensions.register(new TestExt());

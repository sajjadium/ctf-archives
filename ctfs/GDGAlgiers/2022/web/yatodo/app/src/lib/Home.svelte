<script>
  import Settings from "./Settings.svelte";

  let content = "";
  let todoList = [{ content: "Secure this app", completed: true }];

  const addTodo = () => {
    if (content.length > 0) {
      todoList = [...todoList, { content, completed: false }];
      content = "";
    }
  };

  const deleteTodo = (index) => {
    if (index > -1) {
      todoList.splice(index, 1);
      todoList = todoList;
    }
  };
</script>

<Settings heading="Simple todo application" subheading="#MadeWithSvelte💛" />

<div class="card">
  <div>
    {#each todoList as todo, index}
      <div>
        <input bind:checked={todo.completed} type="checkbox" />
        <span class:checked={todo.completed}>{todo.content}</span>
        <button class="button-delete" on:click={() => deleteTodo(index)}
          >-</button
        >
      </div>
    {/each}
  </div>
  <div class="input-div">
    <input bind:value={content} type="text" placeholder="..." />
    <button class="button-add" on:click={addTodo}>+</button>
  </div>
</div>

<style>
  .input-div {
    padding: 5%;
    width: 100%;
  }
  input[type="text"] {
    line-height: 30px;
    width: 100%;
  }
  .checked {
    text-decoration: line-through;
  }
  .button-add {
    background: transparent;
    border: 1px solid rgb(17, 255, 0);
    border-radius: 2em;
    color: rgb(17, 255, 0);
    display: inline-block;
    font-size: 12px;
    height: 20px;
    line-height: 2px;
    margin: 0 0 8px;
    padding: 0;
    text-align: center;
    width: 20px;
  }
  .button-delete {
    background: transparent;
    border: 1px solid rgb(255, 77, 0);
    border-radius: 2em;
    color: rgb(255, 77, 0);
    display: inline-block;
    font-size: 12px;
    height: 20px;
    line-height: 2px;
    margin: 0 0 8px;
    padding: 0;
    text-align: center;
    width: 20px;
  }
</style>

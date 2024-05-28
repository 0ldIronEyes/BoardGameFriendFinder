describe('App Tests', () => {
    let input, suggestions;
  
    beforeAll(() => {

      input = document.createElement('input');
      input.setAttribute('id', 'searchinput');
      document.body.appendChild(input);
  

      suggestions = document.createElement('ul');
      suggestions.classList.add('suggestions');
      const suggestionsContainer = document.createElement('div');
      suggestionsContainer.appendChild(suggestions);
      document.body.appendChild(suggestionsContainer);
    });
  
    afterAll(() => {
      document.body.removeChild(input);
      document.body.removeChild(suggestions);
    });
  
    it('should clear suggestions when input is empty', () => {
      input.value = '';
      const event = new Event('input');
      input.dispatchEvent(event);
  
      expect(suggestions.innerHTML).toBe('');
    });
  
    it('should call search function with input value', async () => {
      spyOn(window, 'search').and.callFake(() => Promise.resolve([]));
  
      input.value = 'test';
      const event = new Event('input');
      input.dispatchEvent(event);
  
      expect(window.search).toHaveBeenCalledWith('test');
    });
  

    it('should show suggestions based on search results', async () => {
      const mockResults = ['Test Game 1', 'Test Game 2'];
      spyOn(window, 'search').and.callFake(() => Promise.resolve(mockResults));
  
      input.value = 'test';
      const event = new Event('input');
      input.dispatchEvent(event);
  
      await new Promise(r => setTimeout(r, 0));
  
      expect(suggestions.childElementCount).toBe(2);
      expect(suggestions.children[0].innerText).toBe('Test Game 1');
      expect(suggestions.children[1].innerText).toBe('Test Game 2');
    });
  


    it('should clear suggestions and set input on click', () => {
      const li = document.createElement('li');
      li.innerText = 'Test Game';
      suggestions.appendChild(li);
  
      const event = new Event('click');
      li.dispatchEvent(event);
  
      expect(input.value).toBe('Test Game');
      expect(suggestions.innerHTML).toBe('');
    });
  });
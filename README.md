# til
Today I Learned
- 1日一つだけ強くなる！


    - run: npm ci
      working-directory: ${{ env.working-dir }}
    - run: npm run build --if-present
      working-directory: ${{ env.working-dir }}
    - run: npm test
      working-directory: ${{ env.working-dir }}
    - run: mv dist ../docs
      working-directory: ${{ env.working-dir }}